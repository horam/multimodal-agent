from types import SimpleNamespace
from typing import List

from multimodal_agent import embedding


class DummyEmbeddingResponse:
    def __init__(self, values):
        self.embeddings = [SimpleNamespace(values=values)]


class DummyModelClient:
    def __init__(self, return_values):
        self._values = return_values

    def embed_content(self, model, contents):
        # Assert usage is correct
        assert isinstance(contents, list)
        assert len(contents) == 1
        return DummyEmbeddingResponse(self._values)


class DummyClient:
    def __init__(self, values):
        self.models = DummyModelClient(return_values=values)


# test methods
def test_embed_text_uses_client_and_returns_list(monkeypatch):
    def fake_get_client():
        return DummyClient([0.1, 0.2, 0.3])

    # Replace get_embedding_client with fake_get_client method.
    monkeypatch.setattr(embedding, "get_embedding_client", fake_get_client)

    vector = embedding.embed_text("hello world", model="test-emb-model")

    assert isinstance(vector, List)
    assert vector == [0.1, 0.2, 0.3]


def test_embed_text_multiple_calls_reuse_client(monkeypatch):
    calls = {"count": 0}

    def fake_get_client():
        # Create a new client after each call.
        calls["count"] += 1
        return DummyClient([0.0])

    monkeypatch.setattr(embedding, "get_embedding_client", fake_get_client)

    vector1 = embedding.embed_text("a")
    vector2 = embedding.embed_text("b")

    assert vector1 == [0.0]
    assert vector2 == [0.0]

    assert calls["count"] >= 1
