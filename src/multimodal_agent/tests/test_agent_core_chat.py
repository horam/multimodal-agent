from multimodal_agent.agent_core import MultiModalAgent, AgentError


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

    # simulate user typing 'hello' then 'exit'
    inputs = ["hello", "exit"]
    monkeypatch.setattr("builtins.input", lambda *_: inputs.pop(0))

    with caplog.at_level("ERROR"):
        agent.chat()

    assert "chat failure" in caplog.text
