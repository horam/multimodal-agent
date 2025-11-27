import pytest

from multimodal_agent import MultiModalAgent
from multimodal_agent.errors import NonRetryableError
from multimodal_agent.utils import load_image_as_part

# Helper fake client for JSON testing
class FakeJSONClient:
    """
    Simulates google-genai client for JSON testing.
    """

    class models:
        @staticmethod
        def generate_content(*args, **kwargs):
            class Resp:
                text = '{"a": 1, "b": "hello"}'

            return Resp()


class FakeMarkdownClient:
    """
    Simulates fenced JSON output.
    """

    class models:
        @staticmethod
        def generate_content(*args, **kwargs):
            class Resp:
                text = '```json\n{"x": 42}\n```'

            return Resp()


class FakeInvalidJSONClient:
    """
    Simulates non-JSON output.
    """

    class models:
        @staticmethod
        def generate_content(*args, **kwargs):
            class Resp:
                text = "this is not json"

            return Resp()


# Test methods
def test_json_response_basic(monkeypatch):
    """Basic JSON dict returned correctly."""
    agent = MultiModalAgent(enable_rag=False)
    agent.client = FakeJSONClient()

    result = agent.ask("hi", response_format="json")

    assert isinstance(result, dict)
    assert result["a"] == 1
    assert result["b"] == "hello"


def test_json_response_markdown_fences_removed(monkeypatch):
    """Handles ```json fenced code blocks correctly."""
    agent = MultiModalAgent(enable_rag=False)
    agent.client = FakeMarkdownClient()

    result = agent.ask("test fenced", response_format="json")

    assert isinstance(result, dict)
    assert result["x"] == 42


def test_json_response_invalid_fallback(monkeypatch):
    """
    Invalid JSON → fallback to {'raw': text}
    """
    agent = MultiModalAgent(enable_rag=False)
    agent.client = FakeInvalidJSONClient()

    result = agent.ask("bad json", response_format="json")

    assert isinstance(result, dict)
    assert "raw" in result
    assert result["raw"] == "this is not json"


def test_json_response_offline_fake_mode(monkeypatch):
    """
    Offline mode (no GOOGLE_API_KEY) returns FakeResponse
    but still JSON-parsed.
    """
    agent = MultiModalAgent(enable_rag=False)

    # Ensure no real API key so FakeResponse is used.
    monkeypatch.setenv("GOOGLE_API_KEY", "")

    result = agent.ask("hello", response_format="json")

    assert isinstance(result, dict)
    # FakeResponse cannot return JSON
    assert "raw" in result


def test_json_response_through_ask_with_image(monkeypatch, tmp_path):
    """
    JSON mode also works with ask_with_image.
    """

    # Create fake 1-byte image
    image_path = tmp_path / "img.jpg"
    image_path.write_bytes(b"\xff\xd8\xff\xd9")

    class DummyImage:
        def __enter__(self):
            return self

        def __exit__(self, *args):
            pass

        def tobytes(self):
            return b"fakeimg"

    # Patch PIL
    monkeypatch.setattr("PIL.Image.open", lambda *_: DummyImage())

    agent = MultiModalAgent(enable_rag=False)
    agent.client = FakeJSONClient()

    part = load_image_as_part(str(image_path))
    result = agent.ask_with_image("describe", part, response_format="json")

    assert isinstance(result, dict)
    assert result["a"] == 1


def test_json_response_real_error_bubbles(monkeypatch):
    """If real client fails, NonRetryableError should be raised."""

    class FailingClient:
        class models:
            @staticmethod
            def generate_content(*args, **kwargs):
                raise Exception("real error")

    agent = MultiModalAgent(enable_rag=False)
    agent.client = FailingClient()

    # Force “real mode” by pretending API key exists
    monkeypatch.setenv("GOOGLE_API_KEY", "dummy_key")

    with pytest.raises(NonRetryableError):
        agent.ask("x", response_format="json")
