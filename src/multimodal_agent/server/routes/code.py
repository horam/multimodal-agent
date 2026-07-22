from fastapi import APIRouter, Depends, HTTPException

from multimodal_agent.server.dependencies import get_engine
from multimodal_agent.server.request_models import (
    ExplainRequest,
    RefactorRequest,
)
from multimodal_agent.server.response_models import RefactorResponse

router = APIRouter(tags=["meta"])


@router.post("/explain", tags=["code"])
def explain_code(request: ExplainRequest, engine=Depends(get_engine)):
    if not request.code.strip():
        raise HTTPException(400, "Code is empty")

    try:
        text = engine.explain_code(request.code)
        return {"text": text}
    except Exception as e:
        raise HTTPException(400, str(e))


@router.post("/refactor", tags=["code"])
def refactor_code(request: RefactorRequest, engine=Depends(get_engine)):
    if not request.code.strip():
        raise HTTPException(400, "Code is empty")

    try:
        text = engine.refactor_code(request.code)
        return RefactorResponse(text=text)
    except Exception as e:
        raise HTTPException(400, str(e))
