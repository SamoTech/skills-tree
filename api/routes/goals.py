#!/usr/bin/env python3
"""GET /goals — list all taxonomy goals."""

from fastapi import APIRouter, HTTPException
from api.dependencies import get_taxonomy
from api.models import GoalsResponse, GoalSummary

router = APIRouter(tags=["Taxonomy"])


@router.get(
    "/goals",
    response_model=GoalsResponse,
    summary="List all taxonomy goals",
    description="Returns all goal categories parsed from GOAL_TAXONOMY.md.",
)
def list_goals() -> GoalsResponse:
    try:
        taxonomy = get_taxonomy()
    except FileNotFoundError as exc:
        raise HTTPException(status_code=503, detail=str(exc))

    goals = [
        GoalSummary(
            id=g["id"],
            name=g["name"],
            description=g.get("description"),
            difficulty=g.get("difficulty"),
            skills_count=g.get("skills_count"),
        )
        for g in taxonomy.list_goals()
    ]
    return GoalsResponse(total=len(goals), goals=goals)
