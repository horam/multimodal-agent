from fastapi import Depends

from multimodal_agent.server.app_state import state


def get_state():
    state.initialize()
    return state


def get_agent(state=Depends(get_state)):
    return state.agent


def get_engine(state=Depends(get_state)):
    return state.engine


def get_rag(state=Depends(get_state)):
    return state.rag
