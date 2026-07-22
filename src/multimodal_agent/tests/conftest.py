import pytest
from fastapi.testclient import TestClient

from multimodal_agent.server.app import create_app
from multimodal_agent.server.app_state import state
from multimodal_agent.server.dependencies import get_agent, get_engine
from multimodal_agent.tests.fakes.agent import FakeAgent
from multimodal_agent.tests.fakes.engine import FakeEngine
from multimodal_agent.tests.fakes.rag import FakeRAG


@pytest.fixture
def fake_agent(fake_rag):
    return FakeAgent(rag_store=fake_rag)


@pytest.fixture
def fake_engine():
    return FakeEngine()


@pytest.fixture
def fake_rag():
    return FakeRAG()


@pytest.fixture
def app(fake_agent, fake_engine):
    state.reload()

    state.agent = fake_agent
    state.engine = fake_engine

    app = create_app()
    app.dependency_overrides[get_agent] = lambda: fake_agent
    app.dependency_overrides[get_engine] = lambda: fake_engine
    return app


@pytest.fixture
def client(app):
    with TestClient(app) as client:
        yield client
    app.dependency_overrides.clear()


@pytest.fixture
def clean_app():
    state.reload()
    app = create_app()
    app.dependency_overrides.clear()
    return app
