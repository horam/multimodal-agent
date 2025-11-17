import sys as system
import types
from unittest.mock import MagicMock

import pytest

from multimodal_agent import __version__, cli


@pytest.fixture(autouse=True)
def mock_google_client(mocker):
    """Mock genai.Client so no real Google API is touched."""
    fake_client = MagicMock()
    fake_client.models.generate_content.return_value = MagicMock(text="mocked")
    mocker.patch(
        "multimodal_agent.agent_core.genai.Client",
        return_value=fake_client,
    )
    return fake_client


# test cli version.
def test_cli_version(monkeypatch, capsys):
    monkeypatch.setattr(system, "argv", ["agent", "--version"])
    cli.main()
    captured = capsys.readouterr().out.strip()

    assert f"multimodal-agent version {__version__}" in captured


# Test text question - ask command
def test_cli_ask(monkeypatch, capsys, mocker):
    fake_agent = types.SimpleNamespace(ask=lambda prompt: f"ANSWER: {prompt}")

    # Patch agent creation
    mocker.patch.object(cli, "MultiModalAgent", return_value=fake_agent)

    monkeypatch.setattr(system, "argv", ["agent", "ask", "hello"])
    cli.main()

    out = capsys.readouterr().out.strip()
    assert "ANSWER: hello" in out


# Test text and image question - image command.
def test_cli_image(monkeypatch, capsys, mocker):
    fake_agent = types.SimpleNamespace(
        ask_with_image=lambda prompt, img: f"IMAGE_ANSWER: {prompt}",
    )

    mocker.patch.object(cli, "MultiModalAgent", return_value=fake_agent)
    mocker.patch.object(cli, "load_image_as_part", return_value="FAKE_PART")

    monkeypatch.setattr(
        system,
        "argv",
        ["agent", "image", "fake.jpg", "describe this"],
    )

    cli.main()
    out = capsys.readouterr().out.strip()

    assert "IMAGE_ANSWER: describe this" in out


# Test invalid image.
def test_cli_image_invalid(monkeypatch, caplog, mocker):
    # Simulate: agent image bad.jpg "prompt"
    monkeypatch.setattr(
        system,
        "argv",
        ["agent", "image", "bad.jpg", "prompt"],
    )

    # 1) Don't let MultiModalAgent hit the real Google client
    fake_agent = mocker.Mock()
    mocker.patch.object(cli, "MultiModalAgent", return_value=fake_agent)

    # 2) Force image loader to fail so we trigger InvalidImageError
    mocker.patch.object(
        cli,
        "load_image_as_part",
        side_effect=Exception("boom"),
    )

    # 3) Route CLI logger into caplog's handler so we can assert on log output
    logger = cli.logger
    logger.handlers = [caplog.handler]
    logger.setLevel("ERROR")

    with caplog.at_level("ERROR"):
        with pytest.raises(SystemExit) as exit_info:
            cli.main()

    # CLI should exit with code 1
    assert exit_info.value.code == 1

    # Collect log messages
    messages = [rec.getMessage() for rec in caplog.records]

    # The outer AgentError handler logs:
    # "Agent failed: Cannot read image: bad.jpg"
    assert any("Cannot read image: bad.jpg" in msg for msg in messages)


# Test chat command.
def test_cli_chat(monkeypatch, mocker):
    fake_agent = types.SimpleNamespace(chat=lambda: None)
    mocker.patch.object(cli, "MultiModalAgent", return_value=fake_agent)

    monkeypatch.setattr(system, "argv", ["agent", "chat"])

    cli.main()  # should run without exception


# Test print_help() scenario.
def test_cli_no_command(monkeypatch, capsys):
    monkeypatch.setattr(system, "argv", ["agent"])

    cli.main()
    out = capsys.readouterr().out

    assert "usage:" in out.lower()
