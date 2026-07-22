import json

from .chunks import FakeChunk


class FakeRAG:
    def __init__(self):
        self.messages: list[FakeChunk] = []
        self.next_id = 1
        self.embeddings = []
        self.searched = []

    def add_logical_message(
        self,
        *,
        content: str,
        role: str,
        session_id: str | None = None,
        source: str | None = None,
    ) -> int:
        chunk = FakeChunk(
            id=self.next_id,
            role=role,
            content=content,
            session_id=session_id,
            source=source,
        )
        self.messages.append(chunk)
        self.next_id += 1

        return [chunk.id]

    def get_recent_chunks(self, limit: int = 50):
        return list(reversed(self.messages))[:limit]

    def search_similar(self, query_embedding, model=None, top_k=5):
        self.searched.append((query_embedding, model, top_k))
        return self.messages[:top_k]

    def load_project_profile(self, project_id):
        if len(self.messages)> 0:
            return json.loads(self.messages[0].content)
        return {"name": "demo"}

    def get_project_profiles(self):
        return []

    def clear(self):
        self.messages.clear()
        self.next_id = 1

    def add_embedding(self, chunk_id, embedding, model):
        self.embeddings.append((chunk_id, tuple(embedding), model))
