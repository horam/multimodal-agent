import json
from pathlib import Path

import requests
from google.genai.types import Blob, Part
from PIL import Image

from multimodal_agent.agent_core import MultiModalAgent
from multimodal_agent.errors import InvalidImageError
from multimodal_agent.rag_store import SQLiteRAGStore, default_db_path


#   IMAGE HELPERS
def load_image_as_part(path: str) -> Part:
    """
    Load a local image file into a Part object.
    """

    path = Path(path)

    if not path.exists():
        raise InvalidImageError(f"Image not found: {path}")

    ext = path.suffix.lower()

    if ext in (".jpg", ".jpeg"):
        mime = "image/jpeg"
    elif ext == ".png":
        mime = "image/png"
    else:
        raise InvalidImageError(f"Unsupported image format: {ext}")

    try:
        with Image.open(path) as image:
            data = image.tobytes()
    except Exception:
        raise InvalidImageError(f"Cannot decode image: {path}")

    return Part(inline_data=Blob(data=data, mime_type=mime))


def load_image_from_url_as_part(url: str, mime_type="image/jpeg") -> Part:
    """
    Load an image from a URL into a Part object.
    """
    response = requests.get(url)
    response.raise_for_status()

    return Part.from_bytes(
        data=response.content,
        mime_type=mime_type,
    )


# Mark down and metadata formatter


def print_markdown_with_meta(
    sections: list[tuple[str, str]],
    meta: dict | None = None,
) -> None:
    """
    Print markdown-formatted sections, then optionally a JSON metadata block.

    sections: list of (title, body) pairs.
    meta: optional dict with machine-readable metadata for tools.
    """
    first = True
    for title, body in sections:
        if not first:
            # print blank line between sections.
            print()
        first = False

        print(f"## {title}\n")
        print(body if body else "(none)")

    if meta is not None:
        print()
        print(json.dumps(meta))


#   HISTORY HANDLERS (RAG-Backed, Session-Aware)
def handle_history(args) -> int:
    """
    Dispatch RAG history operations.
    """
    store = SQLiteRAGStore(default_db_path())
    try:
        if args.history_cmd == "show":
            return _show_history(args, store)
        elif args.history_cmd == "delete":
            return _delete_history(args, store)
        elif args.history_cmd == "clear":
            return _clear_history(args, store)
        elif args.history_cmd == "summary":
            return _summary_history(args, store)
        else:
            print(f"unknown history subcommand: {args.history_cmd}")
            return 1
    finally:
        store.close()


def _show_history(args, store: SQLiteRAGStore) -> int:
    """
    Show stored history from RAG SQLite database.
    """
    chunks = store.get_recent_chunks(limit=args.limit)

    # Filter by session
    if getattr(args, "session", None):
        chunks = [c for c in chunks if c.session_id == args.session]

    if not chunks:
        print_markdown_with_meta(
            sections=[("History", "No history found.")],
            meta={
                "type": "history_show",
                "limit": args.limit,
                "session": getattr(args, "session", None),
                "count": 0,
            },
        )
        return 0

    lines: list[str] = []

    # Reverse chunks in chronological order and generate the content
    for chunk in reversed(chunks):
        session_id = chunk.session_id or "-"
        lines.append(
            f"[{chunk.id}] ({session_id}) {chunk.role} @ {chunk.created_at}",
        )
        # filter content length
        preview = chunk.content[:200]
        lines.append(preview)
        if len(chunk.content) > 200:
            print("  ...")
        lines.append("---")

    body = "\n".join(lines)

    # print content.
    print_markdown_with_meta(
        sections=[("History", body)],
        meta={
            "type": "history_show",
            "limit": args.limit,
            "session": getattr(args, "session", None),
            "count": len(chunks),
        },
    )
    return 0


def _clear_history(args, store: SQLiteRAGStore) -> int:
    store.clear_all()
    print_markdown_with_meta(
        sections=[("History", "History cleared.")],
        meta={"type": "history_clear"},
    )
    return 0


def _delete_history(args, store: SQLiteRAGStore) -> int:
    store.delete_chunk(chunk_id=args.chunk_id)
    print_markdown_with_meta(
        sections=[("History", f"Deleted chunk {args.chunk_id}.")],
        meta={
            "type": "history_delete",
            "chunk_id": args.chunk_id,
        },
    )
    return 0


def _summary_history(args, store: SQLiteRAGStore) -> int:
    """
    Summarize recent history using the LLM.
    """
    chunks = store.get_recent_chunks(limit=args.limit)

    # Filter by session
    if getattr(args, "session", None):
        chunks = [c for c in chunks if c.session_id == args.session]

    if not chunks:
        print_markdown_with_meta(
            sections=[("summary", "No history to summarize.")],
            meta={
                "type": "history_summary",
                "limit": args.limit,
                "session": getattr(args, "session", None),
                "has_history": False,
            },
        )
        return 0

    lines: list[str] = []
    # chronological order
    for chunk in reversed(chunks):
        who = "User" if chunk.role == "user" else "Assistant"
        lines.append(f"{who}: {chunk.content}")

    history_text = "\n".join(lines)

    # Use a fresh agent instance (no RAG needed)
    agent = MultiModalAgent(enable_rag=False)
    prompt = [
        "You are a helpful assistant.",
        "Summarize the following conversation history:",
        history_text,
    ]
    answer = agent.safe_generate_content(prompt)
    summary = answer.text

    print_markdown_with_meta(
        sections=[("Summary", summary)],
        meta={
            "type": "history_summary",
            "limit": args.limit,
            "session": getattr(args, "session", None),
            "has_history": True,
        },
    )
    return 0


# DEPRECATED JSON MEMORY (KEPT FOR BACKWARD COMPATIBILITY)
#
# NOTE: These methods are no longer used now that you have SQLite memory.
# They are kept for compatibility with old code but can be removed
# in a future cleanup release.


MEMORY_PATH = Path.home() / ".multimodal_agent_memory.json"


def append_memory(entry: str) -> None:
    """
    Deprecated: do not use anymore.
    Left for backward compatibility.
    """
    memory = load_memory()
    if not isinstance(memory, list):
        memory = []
    memory.append(entry)
    save_memory(memory=memory)


def delete_memory_index(index: int) -> bool:
    """
    Deprecated: do not use anymore.
    Left for backward compatibility.
    """
    memory = load_memory()
    if index < 0 or index >= len(memory):
        return False
    memory.pop(index)
    save_memory(memory=memory)
    return True


def reset_memory() -> None:
    save_memory([])


def load_memory() -> list[str]:
    """
    Deprecated: do not use anymore.
    Left for backward compatibility.
    """
    if not MEMORY_PATH.exists():
        return []
    try:
        with open(MEMORY_PATH, "r") as f:
            data = json.load(f)
        return data if isinstance(data, list) else []
    except Exception:
        return []


def save_memory(memory: list[str]) -> None:
    """
    Deprecated: do not use anymore.
    Left for backward compatibility.
    """
    MEMORY_PATH.write_text(json.dumps(memory, indent=2))
