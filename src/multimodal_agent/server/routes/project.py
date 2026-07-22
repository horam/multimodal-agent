import json
from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException

from multimodal_agent.project_scanner import scan_project
from multimodal_agent.server.dependencies import get_agent
from multimodal_agent.server.request_models import LearnProjectRequest
from multimodal_agent.server.response_models import (
    LearnProjectResponse,
    ProjectProfileListResponse,
    ProjectProfileResponse,
)

router = APIRouter(tags=["meta"])


# Project learning / profiles
@router.post("/learn/project", tags=["project"])
def learn_project(request: LearnProjectRequest, agent=Depends(get_agent)):
    """
    Learn a project's style profile and optionally store it in RAG.

    This is the HTTP twin of your CLI `learn-project` command and will be
    super useful once your Flutter extension wants to:
    - scan an existing project
    - store its style in RAG
    - then call `/generate` or `/ask` with that style as hidden context
    """
    root = Path(request.path).resolve()
    if not root.exists() or not root.is_dir():
        raise HTTPException(400, f"Invalid project path: {root}")

    # 1. Run scanner
    if request.auto_scan:
        profile = scan_project(root)
    else:
        raise HTTPException(400, "auto_scan=False is not supported yet.")

    profile_dict = profile.to_dict()

    # 2. Optionally store in RAG
    project_id = (
        request.project_id
        or f"project:{profile.package_name or profile.root.name}"  # noqa
    )

    if request.store_profile:
        agent.rag_store.add_logical_message(
            content=json.dumps(profile_dict),
            role="project_profile",
            session_id=project_id,
            source="project-learning",
        )

    return LearnProjectResponse(
        status="ok",
        message="Project learned.",
        project_id=project_id,
        profile=profile_dict,
    )


@router.get("/project_profiles/list", tags=["project"])
def list_project_profiles(agent=Depends(get_agent)):
    """
    List all learned project profiles stored in RAG.
    """
    rows = agent.rag_store.get_project_profiles()
    results = [
        {
            "project_id": row["session_id"],
            "profile": json.loads(row["content"]),
            "created_at": row["created_at"],
        }
        for row in rows
    ]
    return ProjectProfileListResponse(projects=results)


@router.get("/project_profiles/get", tags=["project"])
def get_project_profile(id: str, agent=Depends(get_agent)):
    """
    Get a single project profile by id.
    """
    profile = agent.rag_store.load_project_profile(id)
    if not profile:
        raise HTTPException(404, "Profile not found")
    return ProjectProfileResponse(id=id, profile=profile)


@router.get("/project/{project_id}", tags=["project"])
def load_project_api(project_id: str, agent=Depends(get_agent)):
    """
    Backward-compatible project profile endpoint.
    """
    profile = agent.rag_store.load_project_profile(project_id)
    if not profile:
        raise HTTPException(404, "Not found")
    return ProjectProfileResponse(id=project_id, profile=profile)
