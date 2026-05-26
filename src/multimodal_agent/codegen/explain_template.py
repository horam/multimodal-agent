from textwrap import dedent


def build_explain_prompt(code: str, focus: str | None = None) -> str:
    focus_part = f"\nFocus specifically on {focus}.\n" if focus else ""

    prompt = f"""
    You are a senior Flutter/Dart engineer.

    Task:
    Explain the following Dart code clearly and concisely.

    Rules:
    - Do NOT rewrite the code
    - Do NOT suggest refactors unless asked
    - Explain intent, structure, and responsibilities
    - Be technical but readable{focus_part}

    Code:
    {code}
    """

    return dedent(prompt).strip()
