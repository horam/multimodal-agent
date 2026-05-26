from textwrap import dedent


def build_refactor_prompt(code: str, goal: str | None = None) -> str:
    goal_part = f"\nRefactoring goal: {goal}\n" if goal else ""

    prompt = f"""
    You are an expert Dart engineer following Effective Dart.

    Task:
    Refactor the following Dart code.

    Rules:
    - Output ONLY valid Dart code
    - Preserve behavior
    - Improve clarity, structure, and style
    - No comments, no markdown, no explanation{goal_part}

    Code:
    {code}
    """

    return dedent(prompt).strip()
