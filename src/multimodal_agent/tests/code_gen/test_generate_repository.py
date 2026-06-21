from unittest.mock import patch

from fastapi.testclient import TestClient

from multimodal_agent.codegen.repository_template import (
    build_repository_fallback,
    build_repository_prompt,
)
from multimodal_agent.server import app

client = TestClient(app)


def test_generate_repository_success(tmp_path):
    (tmp_path / "pubspec.yaml").write_text("name: test")

    with patch(
        "multimodal_agent.codegen.engine.CodeGenEngine.generate_repository",
        return_value="abstract class UserRepository {}",
    ):
        response = client.post(
            "/generate/repository",
            json={
                "name": "UserRepository",
                "entity": "User",
                "project_root": str(tmp_path),
            },
        )

    assert response.status_code == 200
    data = response.json()
    assert "code" in data
    assert "UserRepository" in data["code"]


def test_generate_repository_invalid_name(tmp_path):
    (tmp_path / "pubspec.yaml").write_text("name: test")
    with patch(
        "multimodal_agent.codegen.engine.CodeGenEngine.generate_repository",
        return_value="abstract class UserRepository {}",
    ):
        resp = client.post(
            "/generate/repository",
            json={
                "name": "_Repo",
                "project_root": str(tmp_path),
            },
        )

    assert resp.status_code == 400


def test_build_repository_prompt_basic():
    result = build_repository_prompt(raw_name="UserRepository", entity="User")

    assert "UserRepository" in result
    assert "entity `User`" in result
    assert "getAll" in result
    assert "getById" in result
    assert "save" in result
    assert "delete" in result


def test_build_repository_prompt_with_description():

    result = build_repository_prompt(
        raw_name="UserRepository",
        entity="User",
        description="Handles local and remote users",
    )

    assert "Additional repository description from user" in result
    assert "Handles local and remote users" in result


def test_build_repository_prompt_without_entity():
    result = build_repository_prompt(
        raw_name="BaseRepository",
    )

    assert "entity `T`" in result


def test_build_repository_prompt_sanitizes_name():
    result = build_repository_prompt(
        raw_name="user repository",
        entity="user model",
    )

    assert "UserRepository" in result
    assert "UserModel" in result


def test_build_repository_fallback_basic():

    result = build_repository_fallback(
        raw_name="UserRepository",
        entity="User",
    )

    assert "abstract class UserRepository<User>" in result
    assert "Future<List<User>> getAll();" in result
    assert "Future<User?> getById(String id);" in result
    assert "Future<void> save(User entity);" in result
    assert "Future<void> delete(String id);" in result


def test_build_repository_fallback_without_entity():
    result = build_repository_fallback(
        raw_name="BaseRepository",
    )

    assert "abstract class BaseRepository<T>" in result
