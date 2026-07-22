from typing import Optional

from fastapi import APIRouter, Depends

from multimodal_agent.server.dependencies import get_agent
from multimodal_agent.server.request_models import MemorySearchRequest
from multimodal_agent.server.response_models import (
    MemorySearchResponse,
    MemorySummaryResponse,
)

router = APIRouter(prefix="/memory", tags=["meta"])


# Memory / RAG endpoints
@router.post("/search", tags=["memory"])
async def memory_search(
    request: MemorySearchRequest,
    agent=Depends(get_agent),
):
    """
    Vector search over stored memory / RAG store.
    """
    if not agent.enable_rag or agent.rag_store is None:
        return MemorySearchResponse(
            results=[],
            error="RAG disabled",
        )

    results = agent.rag_store.search_similar(
        request.query,
        model=agent.embedding_model,
        top_k=request.limit,
    )
    return MemorySearchResponse(results=results)


@router.post("/summary", tags=["memory"])
@router.get("/summary", tags=["memory"])
async def memory_summary(
    limit: int = 50, session_id: Optional[str] = None, agent=Depends(get_agent)
):
    """
    Summarize recent history / memory.
    We reuse `agent.summarize_history` so behavior is consistent with the CLI.
    """
    if not hasattr(agent, "summarize_history"):
        return MemorySummaryResponse(
            summary="Memory summarization not available.",
        )

    summary = agent.summarize_history(limit=limit, session_id=session_id)
    return MemorySummaryResponse(summary=summary)
