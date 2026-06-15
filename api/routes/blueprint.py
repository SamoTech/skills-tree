#!/usr/bin/env python3
"""POST /blueprint — generate an architecture blueprint for a goal."""

from __future__ import annotations

from fastapi import APIRouter, HTTPException
from api.dependencies import get_engine, get_blueprint_generator, get_taxonomy
from api.models import BlueprintRequest, BlueprintResponse

router = APIRouter(tags=["Blueprints"])


@router.post(
    "/blueprint",
    response_model=BlueprintResponse,
    summary="Generate architecture blueprint",
    description=(
        "Calls BlueprintGenerator with the result from RecommendationEngine. "
        "Returns a full architecture blueprint including required/optional skills, "
        "learning path, risk register, and framework recommendations."
    ),
)
def blueprint(body: BlueprintRequest) -> BlueprintResponse:
    engine    = get_engine()
    generator = get_blueprint_generator()
    taxonomy  = get_taxonomy()

    result = engine.recommend(body.goal)
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])

    bp = generator.generate(body.goal, result, taxonomy)
    return BlueprintResponse(**bp)
