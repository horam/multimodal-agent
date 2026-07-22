# Core text endpoints


from fastapi import APIRouter, Depends

from multimodal_agent.server.dependencies import get_agent
from multimodal_agent.server.request_models import AskRequest, ChatRequest
from multimodal_agent.server.response_models import ChatResponse

router = APIRouter(tags=["meta"])


@router.post("/ask", tags=["core"])
async def ask(request: AskRequest, agent=Depends(get_agent)):
    """
    One-off prompt to the agent.
    """
    response = agent.ask(
        request.prompt,
        response_format=request.response_format or "text",
        session_id=request.session_id,
        rag_enabled=not request.no_rag,
    )
    return ChatResponse(
        text=response.text,
        data=response.data,
        usage=response.usage,
    )


@router.post("/chat", tags=["chat"], response_model=ChatResponse)
async def chat(request: ChatRequest, agent=Depends(get_agent)):
    """
    Chat-style endpoint (single turn) ideal for Flutter extension.

    - Uses `message` instead of `prompt`.
    - Supports optional `session_id` for multi-turn conversations.
    """

    prompt = request.message

    if request.context:
        context = request.context

        context_block = []

        if context.get("language"):
            context_block.append(f"Language: {context['language']}")

        if context.get("fileName"):
            context_block.append(f"File: {context['fileName']}")

        if context.get("selection"):
            context_block.append(f"Selected code:\n{context['selection']}")

        if context_block:
            prompt = (
                "You are assisting a developer inside an IDE.\n\n"
                "Context:\n"
                + "\n".join(f"- {line}" for line in context_block)
                + "\n\nUser question:\n"
                + request.message
            )

    resp = agent.ask(
        prompt,
        response_format=request.response_format or "text",
        session_id=request.session_id,
        rag_enabled=not request.no_rag,
    )

    return ChatResponse(
        text=resp.text,
        data=resp.data,
        usage=resp.usage,
        session_id=request.session_id,
    )
