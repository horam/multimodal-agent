import sys as system
import types
import pytest

from multimodal_agent import cli, __version__


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


# Test invalid image scenario.
def test_cli_image_invalid(monkeypatch, caplog):
    monkeypatch.setattr(
        system,
        "argv",
        ["agent", "image", "bad.jpg", "prompt"],
    )

    # force CLI logger to use caplog handler.
    logger = cli.logger
    # override handlers so caplog can catch the logs.
    logger.handlers = [caplog.handler]
    logger.setLevel("ERROR")

    with caplog.at_level("ERROR"):
        with pytest.raises(SystemExit) as exit_info:
            cli.main()

    assert exit_info.value.code == 1

    messages = [rec.message for rec in caplog.records]

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
