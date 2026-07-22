def test_health(client):
    response = client.get("/health")
    data = response.json()
    assert data["status"] == "ok"
    assert "python" in data
    assert "version" in data
