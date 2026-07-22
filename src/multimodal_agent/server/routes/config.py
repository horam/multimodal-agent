from fastapi import (
    APIRouter,
    Depends,
)

from multimodal_agent import config
from multimodal_agent.server.dependencies import get_agent
from multimodal_agent.server.request_models import (
    ConfigRequest,
    SetupRequest,
)
from multimodal_agent.server.response_models import (
    ConfigResponse,
    GeneralResponse,
)

router = APIRouter(prefix="/config", tags=["meta"])


# agent config.
@router.get("", tags=["config"])
def get_config(agent=Depends(get_agent)):
    cfg = agent.get_config()
    return ConfigResponse(
        configured=bool(cfg.get("api_key")),
        api_key_exists=bool(cfg.get("api_key")),
        chat_model=cfg.get("chat_model"),
    )


@router.post("/setup", tags=["config"])
def setup_config(request: SetupRequest):
    cfg = config.get_config()
    cfg["api_key"] = request.api_key
    config.save_config(cfg)
    return GeneralResponse(success=True)


@router.post("/config", tags=["config"])
def configure_agent(request: ConfigRequest, agent=Depends(get_agent)):
    # Todo: resolve configure method.
    return agent.configure(request)
