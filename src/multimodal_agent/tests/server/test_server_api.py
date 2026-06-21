import io
import os
from types import SimpleNamespace

from fastapi.testclient import TestClient

from multimodal_agent.codegen.engine import CodeGenEngine
from multimodal_agent.server.server import agent, app

client = TestClient(app)


# ask scenarios.
def test_ask(monkeypatch):
    """
    Tests the /ask endpoint with mocked agent.ask().
    """

    def fake_ask(
        prompt,
        response_format=None,
        session_id=None,
        rag_enabled=False,
    ):
        return SimpleNamespace(
            text=f"echo: {prompt}",
            data=None,
            usage={
                "prompt_tokens": 1,
                "response_tokens": 1,
                "total_tokens": 2,
            },
        )

    monkeypatch.setattr(agent, "ask", fake_ask)

    payload = {"prompt": "hello world"}
    resp = client.post("/ask", json=payload)
    data = resp.json()

    assert resp.status_code == 200
    assert data["text"] == "echo: hello world"
    assert data["data"] is None
    assert "usage" in data


def test_ask_with_image(monkeypatch):
    """
    Tests /ask_with_image with mocked ask_with_image and a fake image upload.
    """

    def fake_ask_with_image(prompt, image):
        return SimpleNamespace(
            text="image processed",
            data=None,
            usage={
                "prompt_tokens": 1,
                "response_tokens": 2,
                "total_tokens": 3,
            },
        )

    monkeypatch.setattr(agent, "ask_with_image", fake_ask_with_image)

    fake_image = io.BytesIO(b"\xff\xd8\xff\xd9")

    resp = client.post(
        "/ask_with_image",
        files={"file": ("fake.jpg", fake_image, "image/jpeg")},
        data={"prompt": (None, "describe this")},  # <-- FIXED
    )

    assert resp.status_code == 200
    data = resp.json()
    assert data["text"] == "image processed"
    assert "usage" in data


def test_ask_with_image_agent_failure(monkeypatch):
    def fake_ask_with_image(prompt, image):
        raise RuntimeError("boom")

    monkeypatch.setattr(agent, "ask_with_image", fake_ask_with_image)

    image = io.BytesIO(b"\xff\xd8\xff\xd9")

    response = client.post(
        "/ask_with_image",
        files={"file": ("x.jpg", image, "image/jpeg")},
        data={"prompt": "test"},
    )

    data = response.json()

    assert response.status_code == 200
    assert data["error"] is True
    assert "Image processing failed" in data["text"]


def test_ask_with_image_invalid_upload():
    response = client.post(
        "/ask_with_image",
        data={"prompt": "x"},
    )

    assert response.status_code == 422


def test_generate_json(monkeypatch):
    """
    Tests /generate endpoint with JSON response_format.
    """

    def fake_ask(prompt, response_format="json"):
        return SimpleNamespace(
            text='{"x": 42}',
            data={"x": 42},
            usage=None,
        )

    monkeypatch.setattr(agent, "ask", fake_ask)

    resp = client.post(
        "/generate",
        json={"prompt": "give json", "json": True},
    )
    data = resp.json()

    assert resp.status_code == 200
    assert data["data"] == {"x": 42}
    assert data["text"] == '{"x": 42}'


def test_generate_raw(monkeypatch):
    """
    Tests /generate endpoint when JSON mode = False.
    """

    def fake_ask(prompt, response_format="text"):
        return SimpleNamespace(
            text="raw output",
            data=None,
            usage=None,
        )

    monkeypatch.setattr(agent, "ask", fake_ask)

    resp = client.post("/generate", json={"prompt": "raw test", "json": False})
    data = resp.json()

    assert resp.status_code == 200
    assert data == {"raw": "raw output"}


# Memory scenarios
def test_memory_search(monkeypatch):
    """
    Tests /memory/search endpoint with mocked rag_store.search_similar().
    """

    agent.enable_rag = True

    class FakeStore:
        def search_similar(self, query_embedding, model, top_k):
            return [
                ("0.99", SimpleNamespace(content="hello")),
                ("0.88", SimpleNamespace(content="world")),
            ]

    monkeypatch.setattr(agent, "rag_store", FakeStore())

    resp = client.post("/memory/search", json={"query": "test", "limit": 5})
    data = resp.json()

    assert resp.status_code == 200
    assert "results" in data
    assert len(data["results"]) == 2


def test_memory_search_disabled(monkeypatch):
    """
    Memory search should return error when rag disabled.
    """

    agent.enable_rag = False
    agent.rag_store = None

    resp = client.post("/memory/search", json={"query": "test", "limit": 5})
    data = resp.json()

    assert data["results"] == []
    assert data["error"] == "RAG disabled"


def test_memory_summary(monkeypatch):
    """
    If agent does not have summarize_history(), endpoint should fallback.
    """
    if hasattr(agent, "summarize_history"):
        monkeypatch.delattr(agent, "summarize_history", raising=False)

    resp = client.post("/memory/summary")
    data = resp.json()

    assert resp.status_code == 200
    assert data["summary"] == "Memory summarization not available."


def test_memory_search_arguments(monkeypatch):
    captured = {}

    class FakeStore:
        def search_similar(self, query, model, top_k):
            captured["query"] = query
            captured["top_k"] = top_k
            return []

    monkeypatch.setattr(agent, "rag_store", FakeStore())
    agent.enable_rag = True

    client.post(
        "/memory/search",
        json={"query": "flutter", "limit": 7},
    )

    assert captured["query"] == "flutter"
    assert captured["top_k"] == 7


def test_memory_summary_missing(monkeypatch):
    """
    /memory/summary returns fallback if summarize_history() is missing.
    """

    if hasattr(agent, "summarize_history"):
        monkeypatch.delattr(agent, "summarize_history")

    resp = client.post("/memory/summary")
    data = resp.json()

    assert resp.status_code == 200
    assert data["summary"] == "Memory summarization not available."


# Chat scenarios.
def test_chat_endpoint(monkeypatch):
    def fake_ask(
        prompt,
        response_format=None,
        session_id=None,
        rag_enabled=True,
    ):
        return SimpleNamespace(
            text=f"chat echo: {prompt}",
            data={"ok": True},
            usage={"total_tokens": 5},
        )

    monkeypatch.setattr(agent, "ask", fake_ask)

    resp = client.post("/chat", json={"message": "hello"})
    data = resp.json()

    assert resp.status_code == 200
    assert data["text"] == "chat echo: hello"
    assert data["data"] == {"ok": True}
    assert "usage" in data


def test_chat_with_context(monkeypatch):
    captured = {}

    def fake_ask(prompt, **kwargs):
        captured["prompt"] = prompt

        return SimpleNamespace(
            text="ok",
            data=None,
            usage={},
        )

    monkeypatch.setattr(agent, "ask", fake_ask)

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

    prompt = captured["prompt"]

    assert "Language: dart" in prompt
    assert "File: home.dart" in prompt
    assert "Selected code" in prompt


def test_image_endpoint(monkeypatch):
    def fake_ask_with_image(prompt, image):
        return SimpleNamespace(
            text="image OK",
            data={"detected": "cat"},
            usage={"prompt_tokens": 1},
        )

    monkeypatch.setattr(agent, "ask_with_image", fake_ask_with_image)

    img = io.BytesIO(b"\xff\xd8\xff\xd9")

    resp = client.post(
        "/image",
        files={"file": ("pic.jpg", img, "image/jpeg")},
        data={"prompt": "describe"},
    )

    assert resp.status_code == 200
    data = resp.json()

    assert data["text"] == "image OK"
    assert data["data"] == {"detected": "cat"}


# History scenario.
def test_history_endpoint(monkeypatch):
    class FakeChunk:
        id = 1
        role = "user"
        session_id = "s1"
        content = "hello"
        created_at = "2025-12-01"
        source = None

    class FakeStore:
        def get_recent_chunks(self, limit):
            return [FakeChunk()]

    monkeypatch.setattr(agent, "rag_store", FakeStore())

    resp = client.get("/history?limit=10")
    data = resp.json()

    assert resp.status_code == 200
    assert len(data["items"]) == 1
    assert data["items"][0]["content"] == "hello"


def test_history_summary_endpoint(monkeypatch):
    def fake_summary(limit=50, session_id=None):
        return "summary generated"

    monkeypatch.setattr(
        agent,
        "summarize_history",
        fake_summary,
        raising=False,
    )

    resp = client.get("/history/summary?limit=10")
    data = resp.json()

    assert resp.status_code == 200
    assert data["summary"] == "summary generated"


def test_history_session_filter(monkeypatch):
    class Chunk:
        def __init__(self, sid):
            self.id = 1
            self.role = "user"
            self.session_id = sid
            self.content = sid
            self.created_at = "today"
            self.source = None

    class FakeStore:
        def get_recent_chunks(self, limit):
            return [Chunk("a"), Chunk("b")]

    monkeypatch.setattr(agent, "rag_store", FakeStore())

    response = client.get("/history?session=a")

    data = response.json()

    assert len(data["items"]) == 1
    assert data["items"][0]["content"] == "a"


def test_explain_offline_minimal():
    os.environ.pop("GOOGLE_API_KEY", None)
    code = "class A {}"
    resp = client.post("/explain", json={"code": code})
    assert resp.status_code == 200
    assert "OFFLINE" in resp.json()["text"]


def test_refactor_offline_minimal():
    os.environ.pop("GOOGLE_API_KEY", None)
    code = "class A {}"
    resp = client.post("/refactor", json={"code": code})
    assert resp.status_code == 200
    # offline refactor returns original
    assert resp.json()["text"].strip().startswith("class A")


def test_health():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_learn_project(monkeypatch, tmp_path):
    class FakeProfile:
        package_name = "demo"

        def to_dict(self):
            return {"name": "demo"}

    monkeypatch.setattr(
        "multimodal_agent.server.server.scan_project",
        lambda root: FakeProfile(),
    )

    class FakeStore:
        def add_logical_message(self, **kwargs):
            pass

    monkeypatch.setattr(agent, "rag_store", FakeStore())

    response = client.post(
        "/learn/project",
        json={
            "path": str(tmp_path),
            "auto_scan": True,
            "store_profile": True,
        },
    )

    assert response.status_code == 200


def test_learn_project_invalid_path():
    response = client.post(
        "/learn/project",
        json={
            "path": "/does/not/exist",
            "auto_scan": True,
        },
    )

    assert response.status_code == 400


def test_explain_empty():
    response = client.post("/explain", json={"code": "   "})

    assert response.status_code == 400


def test_generate_widget_invalid_name():
    response = client.post(
        "/generate/widget",
        json={
            "name": "1bad",
            "project_root": ".",
        },
    )

    assert response.status_code == 400


def test_generate_widget_success(monkeypatch, tmp_path):
    # Create fake Flutter project
    (tmp_path / "pubspec.yaml").write_text("name: test_app")

    def fake_generate_widget(
        name,
        stateful=False,
        description="",
    ):
        return """
import 'package:flutter/material.dart';

class MyWidget extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Container();
  }
}
"""

    monkeypatch.setattr(
        CodeGenEngine,
        "generate_widget",
        fake_generate_widget,
    )

    response = client.post(
        "/generate/widget",
        json={
            "name": "MyWidget",
            "project_root": str(tmp_path),
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert "class MyWidget" in data["code"]

    generated = tmp_path / "lib" / "widgets" / "my_widget.dart"

    assert generated.exists()


def test_generate_widget_invalid_root():
    response = client.post(
        "/generate/widget",
        json={"name": "TempName", "project_root": "/bad/path"},
    )

    assert response.status_code == 400


# middleware.
def test_request_id_header():
    response = client.get("/health")
    assert "X-Request-ID" in response.headers


def test_unhandled_exception_route():
    @app.get("/boom")
    def boom():
        raise RuntimeError("crash")

    response = client.get("/boom")

    assert response.status_code == 500
    assert response.json()["detail"] == "Internal server error"
