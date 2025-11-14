import sys
import types

from multimodal_agent import cli


def test_cli_ask_uses_agent(mocker, capsys):
    """
    Test: agent ask "hello"
    - MultiModalAgent.ask should be called with "hello"
    - Output should contain fake response
    """

    # Fake agent with a predictable ask() result
    fake_agent = types.SimpleNamespace(
        ask=lambda prompt: f"FAKE_RESPONSE: {prompt}",
        ask_with_image=None,
        chat=None,
    )

    # Patch MultiModalAgent constructor to return fake agent
    mocker.patch.object(cli, "MultiModalAgent", return_value=fake_agent)

    # Simulate argv: agent ask "hello"
    mocker.patch.object(sys, "argv", ["agent", "ask", "hello"])

    cli.main()
    captured = capsys.readouterr()

    assert "FAKE_RESPONSE: hello" in captured.out


def test_cli_image_uses_loader_and_agent(mocker, capsys):
    """
    Test: agent image /path/img.jpg "describe this"
    - load_image_as_part called with /path/img.jpg
    - ask_with_image called with prompt and fake part
    """

    fake_part = object()

    fake_agent = types.SimpleNamespace(
        ask=None,
        chat=None,
        ask_with_image=lambda prompt, part: f"IMG_RESPONSE: {prompt}",
    )

    mocker.patch.object(cli, "MultiModalAgent", return_value=fake_agent)
    mocker.patch.object(cli, "load_image_as_part", return_value=fake_part)

    mocker.patch.object(
        sys,
        "argv",
        ["agent", "image", "/tmp/fake.jpg", "describe", "this"],
    )

    cli.main()
    captured = capsys.readouterr()

    assert "IMG_RESPONSE: describe this" in captured.out
    cli.load_image_as_part.assert_called_once_with("/tmp/fake.jpg")


def test_cli_chat_calls_agent_chat(mocker, capsys):
    """
    Test: agent chat
    - MultiModalAgent.chat should be called once
    """

    fake_agent = types.SimpleNamespace(
        ask=None, ask_with_image=None, chat=lambda: print("FAKE_CHAT")
    )

    mocker.patch.object(cli, "MultiModalAgent", return_value=fake_agent)
    mocker.patch.object(sys, "argv", ["agent", "chat"])

    cli.main()
    captured = capsys.readouterr()

    assert "FAKE_CHAT" in captured.out
