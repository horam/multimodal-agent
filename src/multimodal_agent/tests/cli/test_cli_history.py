import sys as system
import types
from types import SimpleNamespace

import pytest

import multimodal_agent.cli.cli as cli
from multimodal_agent.cli.history import _is_noise_chunk

moduleName = "multimodal_agent.cli.cli.SQLiteRAGStore"


def make_store(chunks=None):
    return types.SimpleNamespace(
        get_recent_chunks=lambda limit=None: chunks or [],
        delete_chunk=lambda chunk_id=None: None,
        clear_all=lambda: None,
        close=lambda: None,
    )


def test_cli_history_show_empty(monkeypatch, capsys):
    store = make_store()
    monkeypatch.setattr(moduleName, lambda *a, **k: store)
    monkeypatch.setattr(system, "argv", ["agent", "history", "show"])
    cli.main()
    print("output:", capsys.readouterr().out)
    assert "No history" in capsys.readouterr().out


def test_cli_history_delete(monkeypatch, capsys):

    store = make_store()
    store.delete_chunk = lambda **kw: None

    monkeypatch.setattr(moduleName, lambda *a, **k: store)

    monkeypatch.setattr(system, "argv", ["agent", "history", "delete", "2"])
    cli.main()
    out = capsys.readouterr().out

    assert "Deleted chunk 2" in out
    assert '"chunk_id": 2' in out  # also appears in JSON footer


def test_cli_history_reset(monkeypatch, capsys):
    store = make_store()
    monkeypatch.setattr(moduleName, lambda *a, **k: store)
    monkeypatch.setattr(system, "argv", ["agent", "history", "clear"])
    cli.main()
    assert "History cleared" in capsys.readouterr().out


def test_cli_history_summary(monkeypatch, capsys, mocker):
    chunk = SimpleNamespace(
        id=1,
        role="user",
        session_id="s",
        content="hello",
        created_at="2024",
    )
    store = make_store([chunk])

    monkeypatch.setattr(moduleName, lambda *a, **k: store)

    class FakeAgent:
        def __init__(self, *a, **k):
            pass

        def safe_generate_content(self, contents):
            return (SimpleNamespace(text="summary ok"), {"prompt_tokens": 0})

    mocker.patch("multimodal_agent.core.agent_core.MultiModalAgent", FakeAgent)

    monkeypatch.setattr(system, "argv", ["agent", "history", "summary"])
    cli.main()
    out = capsys.readouterr().out
    print("out is: ", out)
    assert "summary ok" in out


def test_cli_history_show_session_filter(monkeypatch, capsys):
    chunks = [
        SimpleNamespace(
            id=1,
            role="user",
            session_id="a",
            content="hello a",
            created_at="2024",
        ),
        SimpleNamespace(
            id=2,
            role="user",
            session_id="b",
            content="hello b",
            created_at="2024",
        ),
    ]

    store = make_store(chunks)

    monkeypatch.setattr(moduleName, lambda *a, **k: store)
    monkeypatch.setattr(
        system,
        "argv",
        ["agent", "history", "show", "--session", "a"],
    )

    cli.main()

    out = capsys.readouterr().out

    assert "hello a" in out
    assert "hello b" not in out


def test_cli_history_show_clean(monkeypatch, capsys):
    chunks = [
        SimpleNamespace(
            id=1,
            role="agent",
            session_id="s",
            content="FAKE_RESPONSE test",
            created_at="2024",
        ),
        SimpleNamespace(
            id=2,
            role="user",
            session_id="s",
            content="real message",
            created_at="2024",
        ),
    ]

    store = make_store(chunks)

    monkeypatch.setattr(moduleName, lambda *a, **k: store)

    monkeypatch.setattr(
        system,
        "argv",
        ["agent", "history", "show", "--clean"],
    )

    cli.main()

    out = capsys.readouterr().out

    assert "real message" in out
    assert "FAKE_RESPONSE" not in out


def test_cli_history_show_long_content(monkeypatch, capsys):
    long_text = "x" * 300

    chunk = SimpleNamespace(
        id=1,
        role="user",
        session_id="s",
        content=long_text,
        created_at="2024",
    )

    store = make_store([chunk])

    monkeypatch.setattr(
        moduleName,
        lambda *a, **k: store,
    )

    monkeypatch.setattr(
        system,
        "argv",
        ["agent", "history", "show"],
    )

    cli.main()

    out = capsys.readouterr().out

    assert "..." in out


def test_cli_history_summary_only_noise(
    monkeypatch,
    capsys,
):
    chunk = SimpleNamespace(
        id=1,
        role="agent",
        session_id="s",
        content="FAKE_RESPONSE mocked",
        created_at="2024",
    )

    store = make_store([chunk])

    monkeypatch.setattr(
        moduleName,
        lambda *a, **k: store,
    )

    monkeypatch.setattr(
        system,
        "argv",
        ["agent", "history", "summary"],
    )

    cli.main()

    out = capsys.readouterr().out

    assert "No meaningful history" in out


def test_cli_history_summary_custom_role(
    monkeypatch,
    capsys,
    mocker,
):
    chunk = SimpleNamespace(
        id=1,
        role="system",
        session_id="s",
        content="system message",
        created_at="2024",
    )

    store = make_store([chunk])

    monkeypatch.setattr(
        moduleName,
        lambda *a, **k: store,
    )

    class FakeAgent:
        def __init__(self, *a, **k):
            pass

        def safe_generate_content(self, contents):
            assert "System: system message" in contents
            return (
                SimpleNamespace(text="summary"),
                {},
            )

    mocker.patch(
        "multimodal_agent.core.agent_core.MultiModalAgent",
        FakeAgent,
    )

    monkeypatch.setattr(
        system,
        "argv",
        ["agent", "history", "summary"],
    )

    cli.main()

    out = capsys.readouterr().out

    assert "summary" in out


@pytest.mark.parametrize(
    "role,content,expected",
    [
        ("user", "hello", False),
        ("agent", "FAKE_RESPONSE xyz", True),
        ("project_profile", "real", True),
        ("agent", "   ", True),
        ("agent", "hi", True),
        ("agent", "mocked response", True),
        ("agent", "real content", False),
    ],
)
def test_is_noise_chunk(role, content, expected):
    chunk = SimpleNamespace(
        role=role,
        content=content,
    )

    assert _is_noise_chunk(chunk) is expected
