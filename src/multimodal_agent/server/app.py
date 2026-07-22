from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from multimodal_agent.server.middleware import register_middlewares
from multimodal_agent.server.routes.chat import router as chat_router
from multimodal_agent.server.routes.code import router as code_router
from multimodal_agent.server.routes.config import router as config_router
from multimodal_agent.server.routes.generate import router as generate_router
from multimodal_agent.server.routes.health import router as health_router
from multimodal_agent.server.routes.history import router as history_router
from multimodal_agent.server.routes.image import router as image_router
from multimodal_agent.server.routes.memory import router as memory_router
from multimodal_agent.server.routes.project import router as project_router


def create_app() -> FastAPI:
    # FastAPI app
    app = FastAPI(
        title="Multimodal Agent Server",
        description="HTTP API for the multimodal-agent (Gemini wrapper + RAG).",
        version="0.1.0",
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
    )
    register_middlewares(app)

    app.include_router(chat_router)
    app.include_router(code_router)
    app.include_router(config_router)
    app.include_router(generate_router)
    app.include_router(health_router)
    app.include_router(history_router)
    app.include_router(image_router)
    app.include_router(memory_router)
    app.include_router(project_router)
    return app
