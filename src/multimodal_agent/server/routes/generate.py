from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException

from multimodal_agent.server.dependencies import get_agent, get_engine
from multimodal_agent.server.request_models import (
    GenerateEnumRequest,
    GenerateModelRequest,
    GenerateRepositoryRequest,
    GenerateRequest,
    GenerateScreenRequest,
    GenerateUseCaseRequest,
    GenerateWidgetRequest,
)
from multimodal_agent.server.response_models import (
    GenerateCodeResponse,
    GenerateResponse,
)

router = APIRouter(prefix="/generate", tags=["meta"])


# Generate endpoint.
@router.post("", tags=["core"])
async def generate(request: GenerateRequest, agent=Depends(get_agent)):
    """
    Generic generate endpoint.

    - If `json=True`, returns `data` + `text`.
    - Otherwise returns a raw string.
    """
    response = agent.ask(
        request.prompt,
        response_format="json" if request.json_response else "text",
    )

    if response.data:
        return GenerateResponse(
            data=response.data,
            text=response.text,
        )

    return GenerateResponse(raw=response.text)


@router.post("/widget", tags=["generate"])
def generate_widget(request: GenerateWidgetRequest, engine=Depends(get_engine)):
    return generate_api_helper(
        request,
        kind="widget",
        engine=engine,
    )


@router.post("/screen", tags=["generate"])
def generate_screen(request: GenerateScreenRequest, engine=Depends(get_engine)):
    return generate_api_helper(
        request,
        kind="screen",
        engine=engine,
    )


@router.post("/model", tags=["generate"])
def generate_model(request: GenerateModelRequest, engine=Depends(get_engine)):
    return generate_api_helper(request, kind="model", engine=engine)


@router.post("/enum", tags=["generate"])
def generate_enum(request: GenerateEnumRequest, engine=Depends(get_engine)):
    return generate_api_helper(request, kind="enum", engine=engine)


@router.post("/repository", tags=["generate"])
def generate_repository(request: GenerateRepositoryRequest, engine=Depends(get_engine)):
    return generate_api_helper(request, kind="repository", engine=engine)


@router.post("/usecase", tags=["generate"])
def generate_usecase(request: GenerateUseCaseRequest, engine=Depends(get_engine)):
    return generate_api_helper(request, kind="usecase", engine=engine)


def generate_api_helper(
    request, kind: str, engine=Depends(get_engine)
) -> GenerateCodeResponse:
    if not request.name or not request.name[0].isalpha():
        raise HTTPException(
            400,
            "Name must start with a letter (valid Dart identifier)",
        )

    try:
        root = Path(request.project_root).resolve()
        if not root.exists():
            raise HTTPException(400, "Invalid project_root")

        path = engine.generate_and_write(
            kind=kind,
            name=request.name,
            root=root,
            override=getattr(request, "override", False),
            stateful=getattr(request, "stateful", False),
            description=request.description or "",
            entity=getattr(request, "entity", None),
            values=getattr(request, "values", None),
        )

        return GenerateCodeResponse(
            code=path.read_text(),
            path=str(path),
        )

    except HTTPException:
        raise
    except Exception as exception:
        # todo(Horam): temporary change.
        message = str(exception)

        if "RESOURCE_EXHAUSTED" in message:
            raise HTTPException(
                429,
                "Gemini API quota exceeded. Please check billing.",
            )
        raise HTTPException(400, str(exception))
