import sys as system

from multimodal_agent import cli


def test_cli_history_show_empty(monkeypatch, capsys):
    """
    When history is empty.
    """
    monkeypatch.setattr(system, "argv", ["agent", "history", "show"])
    monkeypatch.setattr("multimodal_agent.utils.load_memory", lambda: [])

    cli.main()
    output = capsys.readouterr().out
    assert "No history" in output


def test_cli_history_delete(monkeypatch):
    calls = {}

    def fake_delete(index):
        calls["deleted"] = index
        return True

    monkeypatch.setattr(system, "argv", ["agent", "history", "delete", "2"])
    monkeypatch.setattr(
        "multimodal_agent.utils.delete_memory_index",
        fake_delete,
    )

    cli.main()
    assert calls["deleted"] == 2


def test_cli_history_reset(monkeypatch):
    called = {"reset": False}

    monkeypatch.setattr(system, "argv", ["agent", "history", "reset"])
    monkeypatch.setattr(
        "multimodal_agent.utils.reset_memory",
        lambda: called.update(reset=True),
    )

    cli.main()
    assert called["reset"] is True


def test_cli_history_summary(monkeypatch, capsys):
    monkeypatch.setattr(system, "argv", ["agent", "history", "summary"])
    monkeypatch.setattr(
        "multimodal_agent.utils.load_memory",
        lambda: ["USER: hi", "AGENT: hello"],
    )

    class DummyAgent:
        def safe_generate_content(self, contents):
            class R:
                text = "summary ok"

            return R()

    monkeypatch.setattr(
        "multimodal_agent.cli.MultiModalAgent",
        lambda model=None: DummyAgent(),
    )

    cli.main()
    output = capsys.readouterr().out
    assert "summary ok" in output
