import platform

from fastapi import APIRouter

from multimodal_agent import config
from multimodal_agent.server.helpers import get_package_version
from multimodal_agent.server.response_models import HealthResponse

router = APIRouter(tags=["meta"])


# Meta / health
@router.get("/health", tags=["meta"])
def health_check():
    """
    Simple health check for monitoring / Flutter extension.
    """
    cfg = config.get_config()
    return HealthResponse(
        status="ok",
        initialized=bool(cfg.get("api_key")),
        version=get_package_version(),
        python=platform.python_version(),
    )
