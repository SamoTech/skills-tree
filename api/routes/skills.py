#!/usr/bin/env python3
"""GET /skills — list all graph skills."""

from fastapi import APIRouter, HTTPException
from api.dependencies import get_graph
from api.models import SkillsResponse, SkillNode

router = APIRouter(tags=["Skills"])


@router.get(
    "/skills",
    response_model=SkillsResponse,
    summary="List all skills",
    description="Returns all skill nodes from SKILLS_GRAPH.json.",
)
def list_skills() -> SkillsResponse:
    try:
        graph = get_graph()
    except FileNotFoundError as exc:
        raise HTTPException(status_code=503, detail=str(exc))

    skills = [
        SkillNode(
            id=node["id"],
            name=node.get("name", node["id"]),
            category=node.get("category"),
            stability=node.get("stability"),
            description=node.get("description"),
            tags=node.get("tags", []),
        )
        for node in graph.nodes.values()
    ]
    skills.sort(key=lambda s: s.id)
    return SkillsResponse(total=len(skills), skills=skills)
