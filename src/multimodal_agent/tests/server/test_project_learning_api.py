import json


def test_learn_project_endpoint(tmp_path, client):
    # create mock pubspec.yaml
    project = tmp_path / "project"
    project.mkdir()
    (project / "pubspec.yaml").write_text("name: test_project\n")

    response = client.post(
        "/learn/project",
        json={"path": str(project)},
    )
    assert response.status_code == 200

    data = response.json()
    assert data["message"] == "Project learned."
    assert "project_id" in data


def test_load_project_profile(fake_agent, client):
    # Pre-store a fake project profile directly
    project_id = "project:test"
    fake_agent.rag_store.add_logical_message(
        content=json.dumps({"name": "test"}),
        role="project_profile",
        session_id=project_id,
        source="project-learning",
    )

    response = client.get(f"/project/{project_id}")
    print(f"response is {response.json()}")
    assert response.status_code == 200

    data = response.json()
    assert data["id"] == project_id
    assert data["profile"]["name"] == "test"
