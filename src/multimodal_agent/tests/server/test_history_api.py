def test_history_endpoint(fake_agent, client):
    fake_agent.rag_store.add_logical_message(
        content="hello",
        role="user",
        session_id="s1",
    )

    response = client.get("/history?limit=10")
    data = response.json()

    assert response.status_code == 200
    assert len(data["items"]) == 1
    assert data["items"][0]["content"] == "hello"


def test_history_summary_endpoint(fake_agent, monkeypatch, client):
    fake_agent.summarize_history()

    def fake_summary(limit=50, session_id=None):
        return "summary generated"

    monkeypatch.setattr(
        fake_agent,
        "summarize_history",
        fake_summary,
        raising=False,
    )

    response = client.get("/history/summary?limit=10")
    data = response.json()

    assert response.status_code == 200
    assert data["summary"] == "summary generated"


def test_history_session_filter(client, fake_agent):
    fake_agent.rag_store.add_logical_message(
        content="sample content",
        role="user",
        session_id="id",
    )

    response = client.get("/history?session=id")

    data = response.json()

    assert len(data["items"]) == 1
    assert data["items"][0]["content"] == "sample content"
