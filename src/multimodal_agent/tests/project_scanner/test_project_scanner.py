from multimodal_agent.project_scanner import (
    extract_style_profile,
    ingest_style_into_rag,
    scan_project,
)
from multimodal_agent.project_scanner.scanner import ProjectScanner
from multimodal_agent.rag.rag_store import SQLiteRAGStore


def test_full_project_learning_flow(tmp_path):
    proj = tmp_path / "demo"
    proj.mkdir()
    (proj / "pubspec.yaml").write_text("name: demo_app\n")

    scan = scan_project(str(proj))
    style = extract_style_profile(scan)

    rag = SQLiteRAGStore(check_same_thread=False)
    ingest_style_into_rag(style, rag)

    results = rag.search_similar("demo_app", model=None)
    assert isinstance(results, list)


def test_detect_flutter_project(tmp_path):
    project = tmp_path / "flutter_app"
    project.mkdir()
    (project / "pubspec.yaml").write_text(
        """
name: flutter_app
dependencies:
  flutter:
    sdk: flutter
"""
    )
    scanner = ProjectScanner()
    result = scanner.scan(project)

    assert result.is_flutter_project is True


def test_project_without_pubspec(tmp_path):

    project = tmp_path / "empty"
    project.mkdir()
    scanner = ProjectScanner()
    result = scanner.scan(project)

    assert result.package_name is None
    assert result.is_flutter_project is False


def test_detect_clean_architecture(tmp_path):
    project = tmp_path / "app"
    lib = project / "lib"
    (lib / "domain").mkdir(parents=True)
    (lib / "data").mkdir()
    (lib / "presentation").mkdir()
    (project / "pubspec.yaml").write_text("name: test")
    scanner = ProjectScanner()
    result = scanner.scan(project)
    assert "clean_architecture" in result.architecture.patterns


def test_detect_feature_and_modular_architecture(tmp_path):

    project = tmp_path / "app"
    lib = project / "lib"
    (lib / "features").mkdir(parents=True)
    (lib / "modules").mkdir()
    (project / "pubspec.yaml").write_text("name: test")
    scanner = ProjectScanner()
    result = scanner.scan(project)
    assert "feature_first" in result.architecture.patterns
    assert "modular" in result.architecture.patterns


def test_detect_bloc_pattern(tmp_path):

    project = tmp_path / "app"
    lib = project / "lib"
    lib.mkdir(parents=True)
    (lib / "counter_bloc.dart").write_text("class CounterBloc {}")
    (lib / "counter_state.dart").write_text("class CounterState {}")
    (lib / "counter_event.dart").write_text("class CounterEvent {}")
    (project / "pubspec.yaml").write_text(
        """
name: test
dependencies:
  flutter_bloc: ^8.0.0
"""
    )

    scanner = ProjectScanner()
    result = scanner.scan(project)
    assert "bloc_pattern" in result.architecture.patterns
    assert "state_event_pattern" in result.architecture.patterns
    assert "bloc" in result.architecture.state_management


def test_parse_analysis_options(tmp_path):
    project = tmp_path / "app"
    project.mkdir()
    (project / "pubspec.yaml").write_text("name: test")
    (project / "analysis_options.yaml").write_text(
        """
analyzer:
  exclude:
    - build/**
    - "*.g.dart"

linter:
  rules:
    - prefer_single_quotes
    - avoid_print

formatter:
  max_line_length: 120
"""
    )

    scanner = ProjectScanner()
    result = scanner.scan(project)

    lint = result.lint

    assert lint.max_line_length == 120
    assert "prefer_single_quotes" in lint.enabled_rules
    assert "avoid_print" in lint.enabled_rules
    assert "build/**" in lint.excluded_files


def test_scan_dart_files(tmp_path):
    project = tmp_path / "app"
    lib = project / "lib"
    lib.mkdir(parents=True)

    (project / "pubspec.yaml").write_text("name: test")

    (lib / "home.dart").write_text(
        """
import 'package:flutter/widgets.dart';

@freezed
class User {}

@JsonSerializable()
class Product {}

class HomePage extends StatelessWidget {
}
"""
    )

    scanner = ProjectScanner()
    result = scanner.scan(project)

    assert result.dart_files_count == 1
    assert result.widget_files_count == 1
    assert result.uses_freezed is True
    assert result.uses_json_serializable is True


def test_max_files_limit(tmp_path):
    project = tmp_path / "app"
    lib = project / "lib"
    lib.mkdir(parents=True)

    (project / "pubspec.yaml").write_text("name: test")

    for i in range(10):
        (lib / f"file_{i}.dart").write_text("class A {}")

    scanner = ProjectScanner(max_files=5)
    result = scanner.scan(project)

    assert result.dart_files_count == 5
