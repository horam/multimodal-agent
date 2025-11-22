import json
from pathlib import Path

import requests
from google.genai.types import Blob, Part
from PIL import Image

from multimodal_agent.errors import InvalidImageError

MEMORY_PATH = Path.home() / ".multimodal_agent_memory.json"


def append_memory(entry: str) -> None:
    memory = load_memory()
    if not isinstance(memory, list):
        memory = []
    memory.append(entry)
    save_memory(memory=memory)


def delete_memory_index(index: int) -> bool:
    memory = load_memory()
    if index < 0 or index >= len(memory):
        return False
    memory.pop(index)
    save_memory(memory=memory)
    return True


def reset_memory() -> None:
    save_memory("[]")


def load_memory() -> list[str]:
    if not MEMORY_PATH.exists():
        return []
    try:
        with open(MEMORY_PATH, "r") as f:
            data = json.load(f)
        # ensure list
        if not isinstance(data, list):
            return []
        return data
    except Exception:
        return []


def save_memory(memory: list[str]) -> None:
    MEMORY_PATH.write_text(json.dumps(memory, indent=2))


def load_image_as_part(path: str) -> Part:
    """
    Load a local image file into a Part object.
    """

    path = Path(path)

    if not path.exists():
        raise InvalidImageError(f"Image not found: {path}")

    # guess mime
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
        # important: fail loudly
        raise InvalidImageError(f"Cannot decode image: {path}")

    return Part(inline_data=Blob(data=data, mime_type=mime))


def load_image_from_url_as_part(url: str, mime_type="image/jpeg") -> Part:
    """
    Load an image from a URL into a Part object.
    """

    response = requests.get(url)
    response.raise_for_status()  # Ensure we got a successful response

    image_part = Part.from_bytes(
        data=response.content,
        mime_type=mime_type,
    )

    return image_part
