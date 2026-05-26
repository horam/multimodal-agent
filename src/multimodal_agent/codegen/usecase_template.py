from textwrap import dedent

from multimodal_agent.codegen.utils import sanitize_class_name


def build_usecase_prompt(
    raw_name: str,
    entity: str | None = None,
    description: str = "",
) -> str:
    name = sanitize_class_name(raw_name)
    entity_name = sanitize_class_name(entity) if entity else "T"

    extra = f"\nDescription:\n- {description}\n" if description else ""

    prompt = f"""
You are an expert Flutter Clean Architecture developer.

Task:
- Generate a Dart use case class named `{name}`.
- Output MUST be ONLY valid Dart code.
- No markdown, no comments, no explanations.

Requirements:
- Single responsibility
- Callable via call()
- Return Future
- Operate on entity `{entity_name}`{extra}

Output:
Exactly one Dart class named `{name}`.
"""

    return dedent(prompt).strip()


def build_usecase_fallback(
    raw_name: str,
    entity: str | None = None,
) -> str:
    name = sanitize_class_name(raw_name)
    entity_name = sanitize_class_name(entity) if entity else "T"

    return f"""class {name} {{
          const ${name}();
  Future<{entity_name}> call() async {{
    // TODO: implement use case logic
    throw UnimplementedError();
  }}
}}
"""
