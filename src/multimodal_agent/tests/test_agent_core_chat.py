from multimodal_agent.agent_core import AgentError, MultiModalAgent


def test_chat_error_path(monkeypatch, caplog):
    agent = MultiModalAgent(client=None)

    # force generate to always raise AgentError
    def bad_generate(*args, **kwargs):
        raise AgentError("chat failure")

    class DummyClient:
        class models:
            generate_content = bad_generate

    agent.client = DummyClient()

    # Patch the logger so caplog sees its output
    agent.logger.handlers = [caplog.handler]
    agent.logger.setLevel("ERROR")

    monkeypatch.setattr(
        agent.client.models,
        "generate_content",
        lambda *a, **k: (_ for _ in ()).throw(Exception("chat failure")),
    )

    with caplog.at_level("ERROR"):
        agent.chat()

    assert "chat failure" in caplog.text
