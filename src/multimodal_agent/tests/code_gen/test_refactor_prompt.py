from fastapi.testclient import TestClient

from multimodal_agent.codegen.refactor_template import build_refactor_prompt


def test_refactor_code_success(client, fake_engine):
    fake_engine.refactor_response = "class A { const A();}"
    response = client.post(
        "/refactor",
        json={"code": "class A {}"},
    )
    print(f"result is {response.json()}")

    assert response.status_code == 200
    assert "const A()" in response.json()["text"]


def test_refactor_code_offline(monkeypatch, clean_app):

    monkeypatch.delenv("GOOGLE_API_KEY", raising=False)
    client = TestClient(clean_app)

    response = client.post(
        "/refactor",
        json={"code": "class A {}"},
    )

    assert response.status_code == 200
    assert response.json()["text"] == "class A {}"


def test_build_refactor_prompt_without_goal():
    result = build_refactor_prompt(code="class A {}")

    assert "You are an expert Dart engineer" in result
    assert "Refactor the following Dart code." in result
    assert "class A {}" in result
    assert "Refactoring goal:" not in result


def test_build_refactor_prompt_with_goal():
    result = build_refactor_prompt(
        code="class A {}",
        goal="Use const constructors",
    )
    assert "Refactoring goal: Use const constructors" in result
    assert "class A {}" in result


def test_build_refactor_prompt_is_stripped():
    result = build_refactor_prompt(code="class A {}")

    assert result == result.strip()
    assert not result.startswith("\n")
    assert not result.endswith("\n")


def test_build_refactor_prompt_preserves_code_format():

    code = """
class A {
  final int x;
  A(this.x);
}
""".strip()

    result = build_refactor_prompt(code=code)

    assert code in result
