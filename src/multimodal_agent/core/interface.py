from pathlib import Path
from typing import Optional

from multimodal_agent.rag.rag_store import RAGStore, SQLiteRAGStore
from multimodal_agent.utils import MultiModalAgent


def get_agent(
    model="gemini-2.5-flash",
    api_version: str = "v1",
    client=None,
    rag_store: RAGStore | None = None,
    enable_rag: bool = True,
    embedding_model: str = "text-embedding-004",
):
    return MultiModalAgent(
        enable_rag=enable_rag,
        model=model,
        api_version=api_version,
        rag_store=rag_store,
        client=client,
        embedding_model=embedding_model,
    )


def get_sql_rag_store(
    db_path: Optional[str | Path] = None,
    check_same_thread=True,
):
    return SQLiteRAGStore(
        db_path=db_path,
        check_same_thread=check_same_thread,
    )
