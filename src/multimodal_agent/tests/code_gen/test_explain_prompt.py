from unittest.mock import patch

from fastapi.testclient import TestClient

from multimodal_agent.codegen.explain_template import build_explain_prompt
from multimodal_agent.server import app

client = TestClient(app)


def test_build_explain_prompt_contains_code_and_task():
    code = "class X {}"
    prompt = build_explain_prompt(code)

    assert "class X {}" in prompt
    assert "Explain the following Dart code" in prompt
    assert "Do NOT rewrite the code" in prompt


def test_explain_code_success():
    with patch(
        "multimodal_agent.codegen.engine.CodeGenEngine.explain_code",
        return_value="This explains the code.",
    ):
        resp = client.post(
            "/explain",
            json={"code": "class A {}"},
        )

    assert resp.status_code == 200
    data = resp.json()
    assert data["text"] == "This explains the code."


def test_explain_code_offline(monkeypatch):
    monkeypatch.delenv("GOOGLE_API_KEY", raising=False)

    resp = client.post(
        "/explain",
        json={"code": "class A {}"},
    )

    assert resp.status_code == 200
    assert "OFFLINE_EXPLANATION" in resp.json()["text"]
