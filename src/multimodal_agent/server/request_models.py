from typing import Optional

from pydantic import BaseModel, Field


# Request Models
class AskRequest(BaseModel):
    prompt: str
    response_format: str | None = None
    session_id: str | None = None
    no_rag: bool = False


class GenerateRequest(BaseModel):
    """
    Deprecated.
    Generic generate endpoint. Prefer typed endpoints:
    /generate/widget, /generate/screen, /generate/model, ...
    """

    prompt: str
    language: str | None = None
    json_response: bool = True


class MemorySearchRequest(BaseModel):
    query: str
    limit: int = 5


class LearnProjectRequest(BaseModel):
    path: str
    project_id: Optional[str] = None
    auto_scan: bool = True
    store_profile: bool = True
    override_existing: bool = False


class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = None
    no_rag: bool = False
    response_format: Optional[str] = None
    context: Optional[dict] = None


class BaseGenerateRequest(BaseModel):
    name: str = Field(..., description="Dart class name")
    project_root: str = Field(
        ...,
        description="Absolute path to Flutter project root",
        json_schema_extra={
            "example": "Users/owner/projects/my_app",
        },
    )

    description: Optional[str] = Field(
        default=None,
        description="Optional natural language description",
    )
    override: bool = Field(
        default=False,
        description="Overwrite existing file if true",
    )


class GenerateWidgetRequest(BaseGenerateRequest):
    stateful: bool = Field(
        default=False,
        description="Generate StatefulWidget if true",
    )


class GenerateScreenRequest(BaseGenerateRequest):
    pass


class GenerateModelRequest(BaseGenerateRequest):
    pass


class GenerateEnumRequest(BaseGenerateRequest):
    values: Optional[list[str]] = Field(
        default=None,
        description="Optional enum values",
        json_schema_extra={
            "example": ["pending", "paid", "shipped"],
        },
    )


class GenerateRepositoryRequest(BaseGenerateRequest):
    entity: Optional[str] = Field(
        default=None,
        description="Entity name the repository manages",
        json_schema_extra={
            "example": "User",
        },
    )


class GenerateUseCaseRequest(BaseGenerateRequest):
    entity: Optional[str] = Field(
        default=None,
        description="Entity name the usecase manages",
        json_schema_extra={
            "example": "User",
        },
    )


class ExplainRequest(BaseModel):
    code: str


class RefactorRequest(BaseModel):
    code: str


class SetupRequest(BaseModel):
    api_key: str


class ConfigRequest(BaseModel):
    pass
