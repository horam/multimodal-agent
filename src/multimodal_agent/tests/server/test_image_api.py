import io
from types import SimpleNamespace

from multimodal_agent.tests.fakes.response import FakeResponse


def test_ask_with_image(client, fake_agent):
    """
    Tests /ask_with_image with mocked ask_with_image and a fake image upload.
    """
    fake_image = io.BytesIO(b"\xff\xd8\xff\xd9")

    data = {"prompt": (None, "describe this")}

    fake_agent.response = FakeResponse(
        text="image processed",
        data=data,
        usage={
            "prompt_tokens": 1,
            "response_tokens": 1,
            "total_tokens": 2,
        },
    )

    response = client.post(
        "/ask_with_image",
        files={"file": ("fake.jpg", fake_image, "image/jpeg")},
        data=data,
    )

    assert response.status_code == 200
    data = response.json()
    assert data["text"] == "image processed"
    assert "usage" in data


def test_ask_with_image_agent_failure(monkeypatch, client, fake_agent):
    def fake_ask_with_image(prompt, image):
        raise RuntimeError("boom")

    monkeypatch.setattr(fake_agent, "ask_with_image", fake_ask_with_image)

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


def test_ask_with_image_invalid_upload(client):
    response = client.post(
        "/ask_with_image",
        data={"prompt": "x"},
    )

    assert response.status_code == 422


def test_image_endpoint(client, fake_agent):

    fake_agent.response = FakeResponse(
        text="image OK",
        data={"detected": "cat"},
        usage={"prompt_tokens": 1},
    )

    img = io.BytesIO(b"\xff\xd8\xff\xd9")

    response = client.post(
        "/image",
        files={"file": ("pic.jpg", img, "image/jpeg")},
        data={"prompt": "describe"},
    )

    assert response.status_code == 200
    data = response.json()
    assert data["text"] == "image OK"
    assert data["data"] == {"detected": "cat"}
