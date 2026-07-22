from multimodal_agent.project_scanner import scan_project


class FakeProfile:
    package_name = "demo"

    def to_dict(self):
        return {
            "name": "demo",
        }


def test_learn_project(
    monkeypatch,
    tmp_path,
    client,
):
    """
    Test successful project learning flow.

    - scan_project is mocked
    - RAG store is replaced with fake storage
    - endpoint should return 200
    """
    monkeypatch.setattr(
        "multimodal_agent.project_scanner.scan_project",
        lambda root: FakeProfile(),
    )

    response = client.post(
        "/learn/project",
        json={
            "path": str(tmp_path),
            "auto_scan": True,
            "store_profile": False,
        },
    )

    assert response.status_code == 200


def test_learn_project_invalid_path(client):
    """
    Invalid filesystem path should be rejected.
    """

    response = client.post(
        "/learn/project",
        json={
            "path": "/does/not/exist",
            "auto_scan": True,
        },
    )

    assert response.status_code == 400
    assert "detail" in response.json()
