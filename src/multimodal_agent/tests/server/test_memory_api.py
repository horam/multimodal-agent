from multimodal_agent.tests.fakes.rag import FakeChunk


def test_memory_search(fake_agent, client, fake_rag):
    """
    Tests /memory/search endpoint with mocked rag_store.search_similar().
    """
    fake_agent.enable_rag = True
    fake_rag.messages = [
        (0.99, FakeChunk(id=1, role="user", content="hello")),
        (0.88, FakeChunk(id=2, role="user", content="world")),
    ]

    response = client.post(
        "/memory/search",
        json={"query": "test", "limit": 5},
    )
    data = response.json()
    assert response.status_code == 200
    assert "results" in data
    assert len(data["results"]) == 2


def test_memory_search_disabled(fake_agent, client):
    """
    Memory search should return error when rag disabled.
    """

    fake_agent.enable_rag = False
    fake_agent.rag_store = None

    response = client.post("/memory/search", json={"query": "test", "limit": 5})
    data = response.json()

    assert data["results"] == []
    assert data["error"] == "RAG disabled"


def test_memory_summary(monkeypatch, fake_agent, client):
    """
    If agent does not have summarize_history(), endpoint should fallback.
    """
    monkeypatch.delattr(type(fake_agent), "summarize_history", raising=False)

    response = client.post("/memory/summary")
    assert response.status_code == 200
    data = response.json()
    assert data["summary"] == "Memory summarization not available."


def test_memory_search_arguments(fake_agent, monkeypatch, client):
    captured = {}

    class FakeStore:
        def search_similar(self, query, model, top_k):
            captured["query"] = query
            captured["top_k"] = top_k
            return []

    monkeypatch.setattr(fake_agent, "rag_store", FakeStore())
    fake_agent.enable_rag = True

    client.post(
        "/memory/search",
        json={"query": "flutter", "limit": 7},
    )

    assert captured["query"] == "flutter"
    assert captured["top_k"] == 7


def test_memory_summary_missing(fake_agent, monkeypatch, client):
    """
    /memory/summary returns fallback if summarize_history() is missing.
    """

    if hasattr(fake_agent, "summarize_history"):
        monkeypatch.delattr(type(fake_agent), "summarize_history")

    resp = client.post("/memory/summary")
    data = resp.json()

    assert resp.status_code == 200
    assert data["summary"] == "Memory summarization not available."
