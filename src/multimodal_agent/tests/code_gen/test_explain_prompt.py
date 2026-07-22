from fastapi.testclient import TestClient

from multimodal_agent.codegen.engine import CodeGenEngine
from multimodal_agent.codegen.explain_template import build_explain_prompt
from multimodal_agent.server import app


def test_build_explain_prompt_contains_code_and_task():
    code = "class X {}"
    prompt = build_explain_prompt(code)

    assert "class X {}" in prompt
    assert "Explain the following Dart code" in prompt
    assert "Do NOT rewrite the code" in prompt


def test_explain_code_success(client, fake_engine):
    response = client.post(
        "/explain",
        json={"code": "class A {}"},
    )

    assert response.status_code == 200
    data = response.json()
    assert data["text"] == "Explanation"
    assert fake_engine.last_code == "class A {}"


def test_explain_code_offline(monkeypatch, clean_app):
    # clear the dependencies so we can see the impact of deleting keys
    app.dependency_overrides.clear()
    monkeypatch.delenv("GOOGLE_API_KEY", raising=False)
    client = TestClient(clean_app)

    response = client.post(
        "/explain",
        json={"code": "class A {}"},
    )
    assert response.status_code == 200
    assert "OFFLINE_EXPLANATION" in response.json()["text"]
