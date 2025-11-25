from typing import List

from google import genai

_embedding_client = None


def get_embedding_client():
    global _embedding_client
    if _embedding_client is None:
        _embedding_client = genai.Client()
    return _embedding_client


def embed_text(text: str, model: str = "text-embedding-004") -> List[float]:
    """
    Return an embedding vector for the provided text.
    """
    client = get_embedding_client()
    response = client.models.embed_content(
        model=model,
        contents=[text],
    )
    return list(response.embeddings[0].values)
