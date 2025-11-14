import requests
from google.genai.types import Part


def load_image_as_part(path: str, mime_type="image/jpeg") -> Part:
    """
    Load a local image file into a Part object.
    """

    with open(path, "rb") as f:
        image_bytes = f.read()

    image_part = Part.from_bytes(
        data=image_bytes,
        mime_type=mime_type,
    )

    return image_part


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
