import tempfile
from pathlib import Path

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile

from multimodal_agent.server.dependencies import get_agent
from multimodal_agent.server.response_models import ChatResponse
from multimodal_agent.utils import load_image_as_part

router = APIRouter(prefix="", tags=["meta"])


# Image endpoints
@router.post("/ask_with_image")
async def ask_with_image(
    prompt: str = Form(...),
    file: UploadFile = File(...),
    agent=Depends(get_agent),
):
    """
    Accepts an image and text prompt, returns LLM output with robust error
    handling.
    """
    try:
        contents = await file.read()

        # Save temporarily
        suffix = Path(file.filename).suffix or ".jpg"
        with tempfile.NamedTemporaryFile(suffix=suffix, delete=True) as temp:
            temp.write(contents)
            temp.flush()
            image_part = load_image_as_part(temp.name)

        # Try calling LLM
        try:
            response = agent.ask_with_image(prompt, image_part)
            text = response.text or "No text response."
            return ChatResponse(
                text=text,
                data=response.data,
                usage=response.usage,
            )

        except Exception as exception:
            error_message = f"Image processing failed: {str(exception)}"

            usage = (
                getattr(
                    response,
                    "usage",
                    None,
                )
                if "response" in locals()
                else None
            )

            return ChatResponse(
                text=error_message,
                data=None,
                usage=usage,
                error=True,
            )

    except Exception as exception:
        # Critical failure (I/O, file, unexpected)
        raise HTTPException(
            status_code=500,
            detail=f"Server failed to process image: {str(exception)}",
        )


@router.post("/image", tags=["image"])
async def image(
    file: UploadFile = File(...), prompt: str = Form(...), agent=Depends(get_agent)
):
    """
    Convenience alias for /ask_with_image so this works:
    """
    return await ask_with_image(prompt=prompt, file=file, agent=agent)
