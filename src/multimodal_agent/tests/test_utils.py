import pytest

from multimodal_agent.errors import InvalidImageError
from multimodal_agent.utils import load_image_as_part


def test_load_image_invalid(monkeypatch, tmp_path):
    p = tmp_path / "bad.jpg"
    p.write_bytes(b"not-an-image")

    # Force PIL to throw
    monkeypatch.setattr(
        "PIL.Image.open",
        lambda *_: (_ for _ in ()).throw(Exception("fail")),
    )

    with pytest.raises(InvalidImageError):
        load_image_as_part(str(p))


def test_load_image_local_file(monkeypatch, tmp_path):
    p = tmp_path / "test.jpg"
    p.write_bytes(b"fake")

    # Fake PIL Image object
    class DummyImage:
        def __enter__(self):
            return self

        def __exit__(self, *args):
            pass

        def tobytes(self):
            return b"fakeimage"

    monkeypatch.setattr("PIL.Image.open", lambda *_: DummyImage())

    part = load_image_as_part(str(p))

    assert hasattr(part.inline_data, "mime_type")
    assert part.inline_data.mime_type == "image/jpeg"
    assert part.inline_data.data == b"fakeimage"
