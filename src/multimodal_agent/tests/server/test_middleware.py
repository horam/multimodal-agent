from fastapi import APIRouter

router = APIRouter(tags=["meta"])


def test_request_id_header(client):
    response = client.get("/health")
    assert "X-Request-ID" in response.headers


def test_unknown_route_returns_404(client):

    response = client.get("/boom")

    assert response.status_code == 404
    assert response.json()["detail"] == "Not Found"
