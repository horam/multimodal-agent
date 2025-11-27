import os
from typing import List

from google import genai

_embedding_client = None


def get_embedding_client():
    """
    Returns a cached embedding client.
    In tests, this function is monkeypatched to return a DummyClient.
    In real usage, it creates a genai.Client using GOOGLE_API_KEY.
    """
    global _embedding_client

    # If tests monkeypatched this function, they'll bypass this body entirely.
    if _embedding_client is not None:
        return _embedding_client

    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        return None

    _embedding_client = genai.Client(api_key=api_key)
    return _embedding_client


def embed_text(text: str, model: str = "text-embedding-004") -> List[float]:
    """
    Embed a string using Google embeddings API **or** a DummyClient from tests.

    Supports both:
    - Real client
    - DummyClient
    """
    client = get_embedding_client()

    if client is None:
        # In real usage this means RAG embeddings can't run (no API key).
        # Caller (ask/chat) will catch and fall back to non-RAG behavior.
        raise RuntimeError("Missing GOOGLE_API_KEY for embeddings.")

    # Both real client and DummyClient in tests expose `models.embed_content`
    response = client.models.embed_content(model=model, contents=[text])

    # Tests use DummyEmbeddingResponse with `.embeddings[0].values`
    # Real genai client returns Embedding objects that also have `.values`.
    first = response.embeddings[0]
    values = getattr(first, "values", first)

    return list(values)
