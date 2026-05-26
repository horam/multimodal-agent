from unittest.mock import patch

from fastapi.testclient import TestClient

from multimodal_agent.codegen.engine import CodegenEngine
from multimodal_agent.codegen.enum_template import (
    build_enum_fallback,
    build_enum_prompt,
    sanitize_enum_value,
)
from multimodal_agent.server import app

client = TestClient(app)


def test_generate_enum_success(tmp_path):
    (tmp_path / "pubspec.yaml").write_text("name: test")

    with patch(
        "multimodal_agent.codegen.engine.CodegenEngine.generate_enum",
        return_value="enum OrderStatus { pending, shipped }",
    ):
        response = client.post(
            "/generate/enum",
            json={
                "name": "OrderStatus",
                "project_root": str(tmp_path),
            },
        )

    assert response.status_code == 200
    data = response.json()
    assert "code" in data
    assert "enum OrderStatus" in data["code"]


def test_generate_enum_invalid_name(tmp_path):
    (tmp_path / "pubspec.yaml").write_text("name: test")

    response = client.post(
        "/generate/enum",
        json={
            "name": "1BadEnum",
            "project_root": str(tmp_path),
        },
    )

    assert response.status_code == 400
    assert "Name must start with a letter" in response.text


def test_build_enum_prompt_with_value():
    engine = CodegenEngine()
    with patch.object(
        engine,
        "generate_enum",
        return_value="enum OrderStatus { pending, shipped }",
    ):
        result = engine.generate_enum(
            "OrderStatus",
            values=["pending", "shipped"],
        )
    assert "enum OrderStatus" in result
    assert "pending" in result
    assert "shipped" in result


def test_build_enum_prompt_with_values():
    result = build_enum_prompt(
        raw_name="OrderStatus",
        values=["pending", "shipped"],
    )

    assert "OrderStatus" in result
    assert "- pending" in result
    assert "- shipped" in result
    assert "lowerCamelCase" in result


def test_build_enum_prompt_without_values():
    result = build_enum_prompt(
        raw_name="OrderStatus",
    )

    assert "- Choose 3–5 reasonable enum values" in result


def test_build_enum_prompt_with_description():
    result = build_enum_prompt(
        raw_name="OrderStatus",
        values=["pending"],
        description="Used for ecommerce order states",
    )

    assert "Additional description from user" in result
    assert "Used for ecommerce order states" in result


def test_build_enum_prompt_sanitizes_name():
    result = build_enum_prompt(
        raw_name="order status",
    )

    assert "OrderStatus" in result


def test_build_enum_fallback_with_values():
    result = build_enum_fallback(
        raw_name="OrderStatus",
        values=["Pending", "In Progress", "Done"],
    )

    assert "enum OrderStatus" in result
    assert "pending" in result
    assert "in_Progress" in result
    assert "done" in result


def test_build_enum_fallback_without_values():
    result = build_enum_fallback(
        raw_name="Status",
    )
    assert "value1" in result
    assert "value2" in result
    assert "value3" in result


def test_sanitize_enum_value_basic():
    assert sanitize_enum_value("Pending") == "pending"


def test_sanitize_enum_value_with_spaces():
    assert sanitize_enum_value("In Progress") == "in_Progress"


def test_sanitize_enum_value_with_symbols():
    assert sanitize_enum_value("On-Hold!") == "on_Hold_"
