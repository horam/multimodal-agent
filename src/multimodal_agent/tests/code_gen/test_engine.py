import os
import re
from pathlib import Path
from unittest.mock import Mock, patch

import pytest

from multimodal_agent.codegen.engine import CodeGenEngine
from multimodal_agent.codegen.utils import sanitize_class_name, to_snake_case


@pytest.fixture
def fake_engine(monkeypatch):
    """
    Creates a CodeGenEngine with run() patched so we do not call actual LLM.
    run() will return a valid Dart class containing the expected class name.
    """
    engine = CodeGenEngine()

    def fake_run(self, prompt):

        match = re.search(r"named\s+`([A-Za-z0-9_]+)`", prompt)
        if match:
            class_name = match.group(1)
        else:
            class_name = "GeneratedWidget"
        return f"class {class_name} {{}}"

    monkeypatch.setattr(CodeGenEngine, "run", fake_run, raising=True)

    return engine


# Generate and write widget.
def test_generate_and_write_widget(tmp_path: Path, fake_engine: CodeGenEngine):
    # create fake Flutter project
    (tmp_path / "pubspec.yaml").write_text("name: test")

    out = fake_engine.generate_and_write(
        kind="widget",
        name="TestWidget",
        root=tmp_path,
        override=True,
    )

    class_name = sanitize_class_name("TestWidget")
    snake = to_snake_case(class_name)

    expected_path = tmp_path / "lib" / "widgets" / f"{snake}.dart"
    assert out == expected_path
    assert expected_path.exists()

    code = expected_path.read_text()
    assert f"class {class_name}" in code


def test_generate_and_write_screen(tmp_path: Path, fake_engine: CodeGenEngine):
    (tmp_path / "pubspec.yaml").write_text("name: test")

    out = fake_engine.generate_and_write(
        kind="screen",
        name="Home",
        root=tmp_path,
        override=True,
    )

    class_name = sanitize_class_name("Home")
    snake = to_snake_case(class_name)

    expected_path = tmp_path / "lib" / "screens" / f"{snake}_screen.dart"
    assert out == expected_path
    assert expected_path.exists()

    code = expected_path.read_text()
    assert f"class {class_name}" in code


def test_generate_and_write_model(tmp_path: Path, fake_engine: CodeGenEngine):
    (tmp_path / "pubspec.yaml").write_text("name: test")

    out = fake_engine.generate_and_write(
        kind="model",
        name="User",
        root=tmp_path,
        override=True,
    )

    class_name = sanitize_class_name("User")
    snake = to_snake_case(class_name)

    expected_path = tmp_path / "lib" / "models" / f"{snake}.dart"
    assert out == expected_path
    assert expected_path.exists()

    code = expected_path.read_text()
    assert f"class {class_name}" in code


# Imports
def test_insert_material_import_when_missing():
    engine = CodeGenEngine()
    code = "class A {}"
    out = engine.ensure_material_import(code)
    assert "import 'package:flutter/material.dart';" in out


def test_does_not_duplicate_import():
    engine = CodeGenEngine()
    code = "import 'package:flutter/material.dart';\nclass A {}"
    out = engine.ensure_material_import(code)
    assert out.count("material.dart") == 1


# Detect project root.
def test_detect_project_root(tmp_path):
    proj = tmp_path / "myapp"
    proj.mkdir()
    (proj / "pubspec.yaml").write_text("name: test")

    engine = CodeGenEngine()
    root = engine.detect_project_root(proj)

    assert root == proj


def test_detect_project_root_from_child(tmp_path):
    proj = tmp_path / "myapp"
    nested = proj / "lib" / "screens"
    nested.mkdir(parents=True)

    (proj / "pubspec.yaml").write_text("name: test")

    engine = CodeGenEngine()
    root = engine.detect_project_root(nested)

    assert root == proj


def test_detect_project_root_missing(tmp_path):
    engine = CodeGenEngine()
    try:
        engine.detect_project_root(tmp_path)
        assert False, "Expected FileNotFoundError"
    except FileNotFoundError:
        assert True


# Extract code.
def test_extract_code_no_fence():
    engine = CodeGenEngine()
    raw = "class A {}"
    assert engine.extract_code(raw) == "class A {}"


def test_extract_code_with_dart_fence():
    engine = CodeGenEngine()
    raw = "```dart\nclass A {}\n```"
    assert engine.extract_code(raw) == "class A {}"


def test_extract_code_with_plain_fence():
    engine = CodeGenEngine()
    raw = "``` \nclass A {}\n```"
    assert engine.extract_code(raw) == "class A {}"


@patch("multimodal_agent.codegen.engine.get_config")
@patch.dict("os.environ", {}, clear=True)
def test_offline_widget_fallback(mock_config):
    mock_config.return_value = {"api_key": None, "chat_model": "x"}
    engine = CodeGenEngine()
    with patch.object(engine, "is_offline_mode", return_value=True):
        result = engine.generate_and_write(
            kind="widget",
            name="TestWidget",
            root=".",
        )
    assert str(result).endswith(".dart")


@patch("multimodal_agent.codegen.engine.get_config")
@patch.dict("os.environ", {}, clear=True)
def test_offline_screen_fallback(mock_config):
    mock_config.return_value = {"api_key": None, "chat_model": "x"}
    engine = CodeGenEngine()
    with patch.object(engine, "is_offline_mode", return_value=True):
        result = engine.generate_and_write(
            kind="screen",
            name="TestScreen",
            root=".",
        )
    assert str(result).endswith(".dart")


@patch("multimodal_agent.codegen.engine.get_config")
@patch.dict("os.environ", {}, clear=True)
def test_offline_model_fallback(mock_config):
    mock_config.return_value = {"api_key": None, "chat_model": "x"}
    engine = CodeGenEngine()
    with patch.object(engine, "is_offline_mode", return_value=True):
        result = engine.generate_and_write(
            kind="model",
            name="TestModel",
            root=".",
        )
    assert str(result).endswith(".dart")


@patch("multimodal_agent.codegen.engine.get_config")
@patch.dict("os.environ", {}, clear=True)
def test_offline_enum_fallback(mock_config):
    mock_config.return_value = {"api_key": None, "chat_model": "x"}
    engine = CodeGenEngine()
    with patch.object(engine, "is_offline_mode", return_value=True):
        result = engine.generate_and_write(
            kind="enum",
            name="TestEnum",
            root=".",
        )
    assert str(result).endswith(".dart")


@patch("multimodal_agent.codegen.engine.get_config")
@patch.dict("os.environ", {}, clear=True)
def test_offline_repository_fallback(mock_config):
    mock_config.return_value = {"api_key": None, "chat_model": "x"}
    engine = CodeGenEngine()
    with patch.object(engine, "is_offline_mode", return_value=True):
        result = engine.generate_and_write(
            kind="repository",
            name="TestRepository",
            root=".",
        )
    assert str(result).endswith(".dart")


@patch("multimodal_agent.codegen.engine.get_config")
@patch.dict("os.environ", {}, clear=True)
def test_offline_usecase_fallback(mock_config):
    mock_config.return_value = {"api_key": None, "chat_model": "x"}
    engine = CodeGenEngine()
    with patch.object(engine, "is_offline_mode", return_value=True):
        result = engine.generate_and_write(
            kind="usecase",
            name="TestUseCase",
            root=".",
        )
    assert str(result).endswith(".dart")


def test_extract_code_no_fences():
    engine = CodeGenEngine()
    result = engine.extract_code("class A {}")
    assert result == "class A {}"


def test_extract_code_malformed_fences():
    engine = CodeGenEngine()
    result = engine.extract_code("```dart\nclass A {}")
    assert "class A" in result


def test_validate_and_clean_empty():
    engine = CodeGenEngine()
    with pytest.raises(ValueError):
        engine.validate_and_clean("", "User", "widget")


def test_validate_and_clean_missing_class():
    engine = CodeGenEngine()
    code = "class Other {}"
    with pytest.raises(ValueError):
        engine.validate_and_clean(code, "User", "widget")


def test_validate_and_clean_dedup_imports():
    engine = CodeGenEngine()
    code = """
import a;
import a;
class User {}
"""
    result = engine.validate_and_clean(code, "User", "model")
    assert result.count("import a;") == 1


def test_refactor_branch():
    engine = CodeGenEngine()
    with (
        patch.object(engine, "is_offline_mode", return_value=False),
        patch.object(engine, "refactor_code", return_value="refactored"),
    ):

        result = engine._handle_transform(
            kind="refactor",
            name="x",
            root=".",
            code="class A {}",
        )

    assert result == "refactored"


def test_explain_branch():
    engine = CodeGenEngine()
    with (
        patch.object(engine, "is_offline_mode", return_value=False),
        patch.object(engine, "explain_code", return_value="explained"),
    ):

        result = engine._handle_transform(
            kind="explain",
            name="x",
            root=".",
            code="class A {}",
        )

    assert result == "explained"


def test_transform_missing_code():
    engine = CodeGenEngine()
    with pytest.raises(ValueError):
        engine._handle_transform(
            kind="refactor",
            name="x",
            root=".",
        )


def test_run_missing_text():
    engine = CodeGenEngine()

    class Resp:
        pass

    resp = Resp()
    with patch(
        "multimodal_agent.MultiModalAgent",
    ) as mock_agent_cls:
        mock_agent = Mock()
        mock_agent.ask.return_value = resp
        mock_agent_cls.return_value = mock_agent

        with pytest.raises(RuntimeError):
            engine.run("prompt")


def test_material_import_insert_position():
    engine = CodeGenEngine()
    code = """import 'a.dart';
import 'b.dart';
class A {}"""
    out = engine.ensure_material_import(code)

    assert "flutter/material.dart" in out
    assert out.index("material.dart") < out.index("class A")


def test_is_offline_mode_true():
    with (
        patch.dict(os.environ, {}, clear=True),
        patch(
            "multimodal_agent.codegen.engine.get_config",
            return_value={
                "chat_model": "test-model",
                "api_key": None,
            },
        ),
    ):
        engine = CodeGenEngine()
        assert engine.is_offline_mode() is True


def test_is_offline_mode_false_env():
    with (
        patch.dict(os.environ, {"GOOGLE_API_KEY": "key"}),
        patch(
            "multimodal_agent.codegen.engine.get_config",
            return_value={
                "chat_model": "test-model",
                "api_key": None,
            },
        ),
    ):
        engine = CodeGenEngine()
        assert engine.is_offline_mode() is False


def test_generate_and_write_unknown_kind():
    engine = CodeGenEngine()
    with pytest.raises(ValueError):
        engine.generate_and_write(
            kind="unknown",
            name="X",
            root=".",
        )
