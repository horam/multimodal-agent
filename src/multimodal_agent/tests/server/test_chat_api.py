from multimodal_agent.core.agent_core import AgentResponse


def test_ask(client):
    """
    Tests the /ask endpoint with mocked agent.ask().
    """
    response = client.post("/ask", json={"prompt": "hello world"})
    data = response.json()
    assert response.status_code == 200
    assert data["text"] == "echo: hello world"
    assert data["data"] is None
    assert "usage" in data


def test_chat_endpoint(client, fake_agent):

    fake_agent.response = AgentResponse(
        text="chat echo: hello",
        data={"ok": True},
        usage={"total_tokens": 5},
    )

    response = client.post("/chat", json={"message": "hello"})
    data = response.json()

    assert response.status_code == 200
    assert data["text"] == "chat echo: hello"
    assert data["data"] == {"ok": True}
    assert "usage" in data


def test_chat_with_context(fake_agent, client):

    fake_agent.response = AgentResponse(
        text="ok",
        data=None,
        usage={},
    )

    response = client.post(
        "/chat",
        json={
            "message": "Fix this",
            "context": {
                "language": "dart",
                "fileName": "home.dart",
                "selection": "Widget build() {}",
            },
        },
    )

    assert response.status_code == 200

    prompt = fake_agent.last_prompt

    assert "Language: dart" in prompt
    assert "File: home.dart" in prompt
    assert "Selected code" in prompt
