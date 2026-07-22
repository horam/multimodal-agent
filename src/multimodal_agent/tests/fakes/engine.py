import re
from pathlib import Path

from sqlalchemy import desc


class FakeEngine:

    def __init__(self):

        self.last_kind = None
        self.last_name = None
        self.last_code = None
        self.generated_code = "fake generated text"
        self.refactor_response = None

    def explain_code(self, code):
        self.last_code = code
        return "Explanation"

    def refactor_code(self, code):
        self.last_code = code
        if self.refactor_response:
            return self.refactor_response
        return code

    def generate_and_write(
        self,
        kind: str,
        name: str,
        root: str | Path,
        override: bool = False,
        stateful: bool = False,
        description: str = "",
        entity: str | None = None,
        values: list[str] | None = None,
    ):

        self.last_kind = kind
        self.last_name = name
        snake_case = re.sub(
            r"(?<!^)([A-Z])",
            r"_\1",
            name,
        ).lower()

        if kind == "widget":
            path = Path(root) / "lib" / "widgets" / f"{snake_case}.dart"

            code = _fake_generate_widget(
                name,
                stateful,
                description=description,
            )
        elif kind == "screen":
            path = Path(root) / "lib" / "screens" / f"{snake_case}_screen.dart"
            code = _fake_generate_screen(
                name,
                stateful,
                description=description,
            )

        # elif kind == "model":
        #     out_path = root_path / "lib" / "models" / f"{snake_case}.dart"
        #     if self.is_offline_mode():
        #         content = self.generate_fallback_code(
        #             kind=kind,
        #             class_name=class_name,
        #         )

        #     else:
        #         content = self.generate_model(name, description=description)

        # elif kind == "enum":
        #     out_path = root_path / "lib" / "enums" / f"{snake_case}.dart"
        #     if self.is_offline_mode():
        #         content = self.generate_fallback_code(
        #             kind=kind,
        #             class_name=class_name,
        #             values=values,
        #         )
        #     else:
        #         content = self.generate_enum(
        #             name,
        #             description=description,
        #             values=values,
        #         )

        elif kind == "repository":
            path = Path(root) / "lib" / "repositories" / f"{snake_case}.dart"
            code = _fake_generate_repository(
                entity_name=entity,
                repo_name=name,
            )

        elif kind == "usecase":
            path = Path(root) / "lib" / "usecases" / f"{snake_case}.dart"
            code = _fake_generate_usecase(
                entity_name=entity,
                name=name,
            )

        else:
            path = Path(root) / f"{name}.dart"
            code = self.generated_code
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(code)

        return path


def _fake_generate_widget(
    name,
    stateful=False,
    description="",
):

    base = "StatefulWidget" if stateful else "StatelessWidget"

    return f"""
import 'package:flutter/material.dart';

class {name} extends {base} {{
    const {name}({{super.key}});

    @override
    Widget build(BuildContext context) {{
        return Container();
    }}
}}
"""


def _fake_generate_screen(
    name,
    stateful=False,
    description="",
):

    base = "StatefulWidget" if stateful else "StatelessWidget"

    return f"""
import 'package:flutter/material.dart';

class {name} extends {base} {{
    const {name}({{super.key}});

    @override
    Widget build(BuildContext context) {{
        return Container();
    }}
}}
"""


def _fake_generate_repository(repo_name, entity_name):
    return f"""abstract class {repo_name}<{entity_name}> {{
  Future<List<{entity_name}>> getAll();
  Future<{entity_name}?> getById(String id);
  Future<void> save({entity_name} entity);
  Future<void> delete(String id);
}}
"""


def _fake_generate_usecase(name, entity_name):
    return f"""class {name} {{
          const ${name}();
  Future<{entity_name}> call() async {{
    // TODO: implement use case logic
    throw UnimplementedError();
  }}
}}
"""
