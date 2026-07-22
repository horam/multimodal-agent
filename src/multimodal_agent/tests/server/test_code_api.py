import os

from fastapi.testclient import TestClient


def test_explain_offline_minimal(clean_app):
    client = TestClient(clean_app)
    os.environ.pop("GOOGLE_API_KEY", None)
    code = "class A {}"
    response = client.post("/explain", json={"code": code})
    assert response.status_code == 200
    assert "OFFLINE" in response.json()["text"]


def test_refactor_offline_minimal(clean_app):
    client = TestClient(clean_app)
    print(os.environ.get("GOOGLE_API_KEY"))
    os.environ.pop("GOOGLE_API_KEY", None)
    code = "class A {}"
    resp = client.post("/refactor", json={"code": code})
    assert resp.status_code == 200
    # offline refactor returns original
    assert resp.json()["text"].strip().startswith("class A")


def test_explain_empty(client):
    response = client.post("/explain", json={"code": "   "})

    assert response.status_code == 400
