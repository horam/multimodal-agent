from unittest.mock import patch

import pytest

from multimodal_agent.codegen.utils import (
    CodeGenerationError,
    find_flutter_root,
    format_dart_file,
    model_file_path,
    safe_write_file,
    sanitize_class_name,
    screen_file_path,
    to_snake_case,
    widget_file_path,
)


def test_sanitize_class_name_basic():
    assert sanitize_class_name("my widget") == "MyWidget"
    assert sanitize_class_name("my-widget") == "MyWidget"
    assert sanitize_class_name("my_widget") == "MyWidget"


def test_sanitize_class_name_handles_numbers():
    assert sanitize_class_name("123widget") == "W123widget"


def test_sanitize_class_name_empty_input():
    assert sanitize_class_name("") == "GeneratedWidget"


def test_to_snake_case_basic():
    assert to_snake_case("MyWidget") == "my_widget"
    assert to_snake_case("MyWidgetScreen") == "my_widget_screen"


def test_to_snake_case_with_specials():
    assert to_snake_case("my widget") == "my_widget"
    assert to_snake_case("my-widget") == "my_widget"
    assert to_snake_case("my@weird#name") == "myweirdname"


def test_sanitize_removes_invalid_chars():
    assert sanitize_class_name("my@widget!") == "MyWidget"


def test_sanitize_leading_numbers():
    assert sanitize_class_name("42screen") == "W42screen"


def test_sanitize_all_invalid():
    assert sanitize_class_name("@#$%") == "GeneratedWidget"


def test_snake_case_camel_case():
    assert to_snake_case("MyAwesomeWidget") == "my_awesome_widget"


def test_snake_case_removes_specials():
    assert to_snake_case("my@invalid-name!") == "myinvalid_name"


def test_find_flutter_root_success(tmp_path):
    root = tmp_path / "my_app"
    root.mkdir()

    (root / "pubspec.yaml").write_text("name: test")
    (root / "lib").mkdir()

    nested = root / "lib" / "features"
    nested.mkdir(parents=True)

    result = find_flutter_root(nested)

    assert result == root


def test_find_flutter_root_failure(tmp_path):
    with pytest.raises(CodeGenerationError):
        find_flutter_root(tmp_path)


def test_widget_file_path(tmp_path):
    result = widget_file_path(tmp_path, "MyWidget")

    assert result == tmp_path / "lib" / "widgets" / "my_widget.dart"


def test_screen_file_path(tmp_path):
    result = screen_file_path(tmp_path, "HomeScreen")

    assert result == tmp_path / "lib" / "screens" / "home_screen.dart"


def test_model_file_path(tmp_path):
    result = model_file_path(tmp_path, "UserModel")

    assert result == tmp_path / "lib" / "models" / "user_model.dart"


def test_safe_write_file_creates_file(tmp_path):
    file_path = tmp_path / "test.dart"

    safe_write_file(
        file_path,
        "class Test {}",
        run_format=False,
    )

    assert file_path.exists()
    assert file_path.read_text() == "class Test {}"


def test_safe_write_file_prevents_override(tmp_path):
    file_path = tmp_path / "test.dart"
    file_path.write_text("old")

    with pytest.raises(CodeGenerationError):
        safe_write_file(
            file_path,
            "new",
            override=False,
            run_format=False,
        )


def test_safe_write_file_override_enabled(tmp_path):
    file_path = tmp_path / "test.dart"
    file_path.write_text("old")

    safe_write_file(
        file_path,
        "new",
        override=True,
        run_format=False,
    )

    assert file_path.read_text() == "new"


def test_safe_write_file_calls_formatter(tmp_path):
    file_path = tmp_path / "test.dart"

    with patch(
        "multimodal_agent.codegen.utils.format_dart_file",
    ) as mock_format:
        safe_write_file(
            file_path,
            "class Test {}",
            run_format=True,
        )

    mock_format.assert_called_once_with(file_path)


def test_safe_write_file_skips_formatter_for_non_dart(tmp_path):
    file_path = tmp_path / "test.txt"

    with patch(
        "multimodal_agent.codegen.utils.format_dart_file",
    ) as mock_format:
        safe_write_file(
            file_path,
            "hello",
            run_format=True,
        )

    mock_format.assert_not_called()


def test_format_dart_file_calls_subprocess(tmp_path):
    file_path = tmp_path / "test.dart"
    file_path.write_text("class Test{}")

    with patch("multimodal_agent.codegen.utils.subprocess.run") as mock_run:
        format_dart_file(file_path)

    mock_run.assert_called_once()


def test_format_dart_file_swallows_exception(tmp_path):
    file_path = tmp_path / "test.dart"

    with patch(
        "multimodal_agent.codegen.utils.subprocess.run",
        side_effect=Exception("dart missing"),
    ):
        format_dart_file(file_path)
