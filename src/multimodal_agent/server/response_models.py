from typing import Any, Dict, List, Optional, Tuple

from pydantic import BaseModel


# Response Models
class ChatResponse(BaseModel):
    text: Optional[str] = None
    data: Optional[Dict[str, Any]] = None
    usage: Optional[Dict[str, Any]] = None
    session_id: Optional[str] = None
    error: Optional[bool] = False


class HistoryItem(BaseModel):
    id: int
    role: str
    session_id: Optional[str]
    content: str
    created_at: str
    source: Optional[str] = None


class HistoryResponse(BaseModel):
    items: List[HistoryItem]
    limit: int
    session: Optional[str] = None


class SummaryResponse(BaseModel):
    summary: str
    limit: int
    session: Optional[str] = None


class MemorySummaryResponse(BaseModel):
    summary: str


class ConfigResponse(BaseModel):
    configured: bool
    api_key_exists: bool
    chat_model: str | None = None
    model: list[str] | None = None


class GenerateCodeResponse(BaseModel):
    code: str
    path: Optional[str] = None


class GenerateResponse(BaseModel):
    data: Optional[str] = None
    raw: Optional[str] = None
    text: Optional[str] = None


class MemorySearchResponse(BaseModel):
    results: List[Tuple]
    error: Optional[str] = None


class LearnProjectResponse(BaseModel):
    status: str
    message: str
    project_id: str
    profile: Dict[str, Any]


class ProjectProfileResponse(BaseModel):
    id: str
    profile: Any


class ProjectProfileListResponse(BaseModel):
    projects: List[dict[str, Any]]


class ExplainResponse(BaseModel):
    text: str


class RefactorResponse(BaseModel):
    text: str


class GeneralResponse(BaseModel):
    success: Optional[str] = None


class HealthResponse(BaseModel):
    status: str
    initialized: bool
    version: str
    python: str
