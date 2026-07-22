from types import SimpleNamespace

from multimodal_agent.codegen.engine import CodeGenEngine
from multimodal_agent.tests.fakes import agent
from multimodal_agent.tests.fakes.response import FakeResponse


def test_generate_json(client, fake_agent):
    """
    Tests /generate endpoint with JSON response_format.
    """

    fake_agent.response = FakeResponse(
        text='{"x": 42}',
        data="temp data",
        usage=None,
    )

    response = client.post(
        "/generate",
        json={"prompt": "give json", "json": True},
    )
    data = response.json()

    assert response.status_code == 200
    assert data["data"] == "temp data"
    assert data["text"] == '{"x": 42}'


def test_generate_raw(client, fake_agent):
    """
    Tests /generate endpoint when JSON mode = False.
    """

    fake_agent.response = FakeResponse(
        text="raw output",
        data=None,
        usage=None,
    )

    response = client.post(
        "/generate",
        json={
            "prompt": "raw test",
            "json": False,
        },
    )
    data = response.json()
    assert response.status_code == 200
    assert data["raw"] == "raw output"


def test_generate_widget_invalid_name(client):
    response = client.post(
        "/generate/widget",
        json={
            "name": "1bad",
            "project_root": ".",
        },
    )

    assert response.status_code == 400


def test_generate_widget_success(tmp_path, client):
    # Create fake Flutter project
    (tmp_path / "pubspec.yaml").write_text("name: test_app")

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


def test_generate_widget_invalid_root(client):
    response = client.post(
        "/generate/widget",
        json={"name": "TempName", "project_root": "/bad/path"},
    )

    assert response.status_code == 400
