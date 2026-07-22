import builtins

import pytest

from multimodal_agent.core import agent_core
from multimodal_agent.core.interface import get_agent
from multimodal_agent.errors import NonRetryableError, RetryableError
from multimodal_agent.tests.fakes.client import FakeClient
from multimodal_agent.tests.fakes.image import FakeImage
from multimodal_agent.tests.fakes.response import FakeResponse
from multimodal_agent.utils import load_image_as_part


def test_task_text(fake_agent):
    response = fake_agent.ask("hello")
    assert response.text == "echo: hello"


def test_task_with_image(fake_agent, tmp_path, monkeypatch):
    image_path = tmp_path / "img.jpg"
    # Fake image bytes.
    image_path.write_bytes(b"\xff\xd8\xff\xd9")

    # Mock PIL.Image.open so decoding always succeeds.

    monkeypatch.setattr("PIL.Image.open", lambda *_: FakeImage())

    image_part = load_image_as_part(str(image_path))

    response = fake_agent.ask_with_image("describe", image_part)
    assert response.text == "echo: describe"


def test_chat_history_format(client, mocker):
    """
    Ensure chat appends text to history correctly.
    """

    agent = get_agent(client=client, enable_rag=False, rag_store=None)

    # simulate user input twice then exit
    mocker.patch("builtins.input", side_effect=["hello", "exit"])

    # MUST return AgentResponse, not plain object
    agent.safe_generate_content = lambda contents: (
        type("R", (), {"text": "reply"})(),
        None,
    )

    agent.chat()


def test_agent_init_uses_dummy_client_when_no_api_key(monkeypatch):
    monkeypatch.delenv("GOOGLE_API_KEY", raising=False)

    # IMPORTANT: config may contain an api_key → must neutralize it
    monkeypatch.setattr(agent_core, "get_config", lambda: {})

    agent = get_agent(client=None, enable_rag=False, rag_store=None)

    assert hasattr(agent.client, "models")
    with pytest.raises(RuntimeError):
        agent.client.models.generate_content(model="x", contents=["y"])


# ask_with_image JSON path + _parse_json_output exception
def test_ask_with_image_json_parse_error_falls_back_to_none(monkeypatch, fake_agent):
    # Online mode client
    monkeypatch.setenv("GOOGLE_API_KEY", "dummy-key")

    agent = get_agent(
        client=FakeClient(text="```json {not-valid-json} ```"),
        enable_rag=False,
        rag_store=None,
    )
    agent.usage_logging = False

    # Force _parse_json_output to raise → we want data = None
    def boom(_text):
        raise ValueError("bad json")

    monkeypatch.setattr(agent, "_parse_json_output", boom)

    # Dummy 'image' (no need to be real Part; runtime doesn't enforce type)
    dummy_image = object()

    resp = agent.ask_with_image(
        "question",
        dummy_image,
        response_format="json",
    )
    assert isinstance(resp.text, str)
    assert resp.data is None  # came from the except-branch


def test_ask_json_with_rag_calls_store_agent_reply(fake_rag, monkeypatch):

    monkeypatch.setenv("GOOGLE_API_KEY", "dummy-key")

    client = FakeClient(text='{"answer": 42}')

    agent = get_agent(
        client=client,
        rag_store=fake_rag,
        enable_rag=True,
    )
    agent.usage_logging = False

    # Fake embed_text so it doesn't hit the real API
    monkeypatch.setattr(
        agent_core,
        "embed_text",
        lambda text, model: [0.1, 0.2],
    )

    response = agent.ask(
        "What is life?",
        session_id="sess-1",
        response_format="json",
    )
    

    assert response.text == '{"answer": 42}'
    # Question + agent reply should be stored
    roles = [message.role for message in fake_rag.messages]
    assert "user" in roles
    assert "agent" in roles


def test_ensure_session_id_returns_given_value(client):
    agent = get_agent(
        client=client,
        enable_rag=False,
        rag_store=None,
    )
    assert agent._ensure_session_id("custom") == "custom"


def test_convert_to_json_response_parses_valid_json(client):
    agent = get_agent(
        client=client,
        enable_rag=False,
        rag_store=None,
    )
    response = FakeResponse(text='{"x": 1}')

    out = agent._convert_to_json_response(response)
    assert out.json == {"x": 1}


def test_convert_to_json_response_fallback_raw(client):
    agent = get_agent(
        client=client,
        enable_rag=False,
        rag_store=None,
    )

    response = FakeResponse(text="not-json")

    out = agent._convert_to_json_response(response)
    assert out.json == {"raw": "not-json"}


def test_parse_json_output_handles_fenced_block(client):
    agent = get_agent(
        client=client,
        enable_rag=False,
        rag_store=None,
    )
    text = '```json\n{"a": 1}\n```'
    parsed = agent._parse_json_output(text)
    assert parsed == {"a": 1}


def test_parse_json_output_trailing_backticks_only(client):
    agent = get_agent(
        client=client,
        enable_rag=False,
        rag_store=None,
    )
    text = 'json {"b": 2}```'
    parsed = agent._parse_json_output(text)
    assert parsed == {"b": 2}


def test_strip_markdown_removes_fence_and_json_prefix(client):
    agent = get_agent(
        client=client,
        enable_rag=False,
        rag_store=None,
    )
    raw = '```json\n{"c": 3}\n```'
    cleaned = agent._strip_markdown(raw)
    assert cleaned == '{"c": 3}'


def test_store_agent_reply_catches_embedding_errors(monkeypatch, client, fake_rag):
    agent = get_agent(
        client=client,
        rag_store=fake_rag,
        enable_rag=True,
    )

    # embed_text should blow up → we want except-block to swallow it
    def boom(text, model):
        raise RuntimeError("embed failed")

    monkeypatch.setattr(agent_core, "embed_text", boom)

    # Should not raise
    agent._store_agent_reply(answer={"foo": "bar"}, session_id="sess-2")
    print(f"messages: {fake_rag.messages}")

    # Message still stored
    assert any(message.role == "agent" for message in fake_rag.messages)


def test_log_usage_ignores_file_errors(monkeypatch, client):
    agent = get_agent(
        client=client,
        enable_rag=False,
        rag_store=None,
    )

    def fake_open(*args, **kwargs):
        raise IOError("disk full")

    monkeypatch.setattr(builtins, "open", fake_open)

    # Should not raise even if open() fails
    agent._log_usage(
        usage={"prompt_tokens": 1, "response_tokens": 2, "total_tokens": 3},
        contents=["hi"],
        response_format="text",
        model="dummy",
    )


def test_chat_embedding_failure_and_assistant_embed_failure(
    monkeypatch, client, fake_rag
):
    """
    Covers:
    - question_embedding exception → question_embedding = None (485–486)
    - rag_context = [] (490)
    - assistant reply embedding exception in chat (566–567)
    """
    agent = get_agent(
        client=client,
        rag_store=fake_rag,
        enable_rag=True,
    )

    calls = []

    def boom(text, model):
        calls.append(text)
        raise RuntimeError("embed failed")

    monkeypatch.setattr(
        agent_core,
        "embed_text",
        boom,
    )

    # Simulate one user message then exit.
    inputs = iter(["hello", "exit"])
    monkeypatch.setattr("builtins.input", lambda _prompt: next(inputs))
    agent.chat(session_id="chat-sess-1", enable_rag=True, rag_top_k=3)
    assert len(calls) > 0


def test_chat_handles_retryable_error(monkeypatch, client):
    """
    Covers except RetryableError (533–534).
    """
    agent = get_agent(
        client=client,
        rag_store=None,
        enable_rag=False,
    )

    calls = []

    def raise_retryable(*args, **kwargs):
        calls.append(True)
        raise RetryableError("temporary")

    monkeypatch.setattr(
        agent,
        "safe_generate_content",
        raise_retryable,
    )

    inputs = iter(["hello", "exit"])

    monkeypatch.setattr(
        "builtins.input",
        lambda _prompt: next(inputs),
    )

    agent.chat(
        session_id="chat-sess-3",
        enable_rag=False,
    )

    assert len(calls) == 1


def test_chat_handles_non_retryable_error(monkeypatch, client):
    """
    Covers except NonRetryableError (540–542).
    """

    agent = get_agent(
        client=client,
        rag_store=None,
        enable_rag=False,
    )

    calls = []

    def raise_non_retryable(*args, **kwargs):
        calls.append(True)
        raise NonRetryableError("permanent")

    monkeypatch.setattr(
        agent,
        "safe_generate_content",
        raise_non_retryable,
    )

    inputs = iter(["hello", "exit"])
    monkeypatch.setattr(
        "builtins.input",
        lambda _prompt: next(inputs),
    )

    agent.chat(
        session_id="chat-sess-4",
        enable_rag=False,
    )

    assert len(calls) == 1
