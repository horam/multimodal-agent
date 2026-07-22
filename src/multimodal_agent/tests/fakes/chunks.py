from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class FakeChunk:
    id: int
    role: str
    content: str
    session_id: str | None = None
    source: str | None = None
    created_at: datetime = field(default_factory=datetime.now)
