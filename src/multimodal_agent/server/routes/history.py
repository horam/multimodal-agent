from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query

from multimodal_agent.server.dependencies import get_agent
from multimodal_agent.server.response_models import (
    HistoryItem,
    HistoryResponse,
    SummaryResponse,
)

router = APIRouter(prefix="/history", tags=["meta"])


def _serialize_chunk(chunk) -> HistoryItem:
    return HistoryItem(
        id=chunk.id,
        role=chunk.role,
        session_id=getattr(chunk, "session_id", None),
        content=chunk.content,
        created_at=str(chunk.created_at),
        source=getattr(chunk, "source", None),
    )


@router.get("", tags=["history"], response_model=HistoryResponse)
def history(
    limit: int = Query(50, ge=1),
    session: Optional[str] = Query(None),
    agent=Depends(get_agent),
):
    """
    Get recent history from the SQLite RAG store.

    This is useful for:
    - Inspecting what the CLI / agents have stored
    - Feeding context into your Flutter extension if you want an external
    viewer
    """
    if agent.rag_store is None:
        raise HTTPException(400, "RAG store not available")

    chunks = agent.rag_store.get_recent_chunks(limit=limit)

    if session:
        chunks = [
            chunk
            for chunk in chunks
            if getattr(chunk, "session_id", None) == session  # noqa
        ]

    items = [_serialize_chunk(c) for c in chunks]

    return HistoryResponse(
        items=items,
        limit=limit,
        session=session,
    )


@router.get(
    "/summary",
    tags=["history"],
    response_model=SummaryResponse,
)
def history_summary(
    limit: int = Query(50, ge=1),
    session: Optional[str] = Query(None),
    agent=Depends(get_agent),
):
    """
    Summarize history using the same summarizer used by the CLI.
    """
    if not hasattr(agent, "summarize_history"):
        raise HTTPException(
            status_code=400,
            detail="History summarization not available on this agent.",
        )

    summary = agent.summarize_history(limit=limit, session_id=session)
    return SummaryResponse(
        summary=summary,
        limit=limit,
        session=session,
    )
