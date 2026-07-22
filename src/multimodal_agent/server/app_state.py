import os
from typing import Optional

from multimodal_agent import MultiModalAgent, config
from multimodal_agent.codegen.engine import CodeGenEngine
from multimodal_agent.core.interface import get_agent
from multimodal_agent.rag.rag_store import SQLiteRAGStore


class AppState:
    def __init__(self):
        self.agent: Optional[MultiModalAgent] = None
        self.engine: Optional[CodeGenEngine] = None
        self.rag: Optional[SQLiteRAGStore] = None

    def initialize(self):
        if self.agent is not None:
            return

        self.rag = SQLiteRAGStore(
            db_path=os.environ.get("MULTIMODAL_AGENT_DB", ":memory:"),
            check_same_thread=False,
        )

        self.agent = get_agent(
            rag_store=self.rag,
            enable_rag=True,
        )

        engine_config = config.get_config()

        self.engine = CodeGenEngine(model=engine_config["chat_model"])

    def reload(self):
        self.agent = None
        self.engine = None
        self.rag = None


state = AppState()
