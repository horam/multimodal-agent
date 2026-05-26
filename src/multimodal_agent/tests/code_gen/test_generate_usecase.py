from unittest.mock import patch

from fastapi.testclient import TestClient

from multimodal_agent.codegen.usecase_template import build_usecase_prompt
from multimodal_agent.server import app

client = TestClient(app)


def test_usecase_prompt_contains_name_and_entity():
    prompt = build_usecase_prompt("FetchUser", entity="User")
    assert "FetchUser" in prompt
    assert "entity `User`" in prompt


def test_generate_usecase_success(tmp_path):
    (tmp_path / "pubspec.yaml").write_text("name: test")

    with patch(
        "multimodal_agent.codegen.engine.CodegenEngine.generate_usecase",
        return_value="class FetchUser { Future<User> call() async {} }",
    ):
        response = client.post(
            "/generate/usecase",
            json={
                "name": "FetchUser",
                "entity": "User",
                "project_root": str(tmp_path),
            },
        )

    assert response.status_code == 200
    assert "FetchUser" in response.json()["code"]


def test_generate_usecase_offline(monkeypatch, tmp_path):
    (tmp_path / "pubspec.yaml").write_text("name: test")
    monkeypatch.delenv("GOOGLE_API_KEY", raising=False)

    resp = client.post(
        "/generate/usecase",
        json={
            "name": "FetchUser",
            "entity": "User",
            "project_root": str(tmp_path),
        },
    )

    assert resp.status_code == 200
    assert "class FetchUser" in resp.json()["code"]
