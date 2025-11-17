import requests
from pathlib import Path
from google.genai.types import Part, Blob
from multimodal_agent.errors import InvalidImageError

from PIL import Image


def load_image_as_part(path: str) -> Part:
    """
    Load a local image file into a Part object.
    """

    p = Path(path)

    if not p.exists():
        raise InvalidImageError(f"Image not found: {path}")

    # guess mime
    ext = p.suffix.lower()
    if ext in (".jpg", ".jpeg"):
        mime = "image/jpeg"
    elif ext == ".png":
        mime = "image/png"
    else:
        raise InvalidImageError(f"Unsupported image format: {ext}")

    try:
        with Image.open(p) as img:
            data = img.tobytes()
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
