#!/usr/bin/env python3
"""GET /health — liveness probe."""

from fastapi import APIRouter
from api.models import HealthResponse

router = APIRouter(tags=["System"])


@router.get(
    "/health",
    response_model=HealthResponse,
    summary="Health check",
    description="Returns API liveness status and current version.",
)
def health() -> HealthResponse:
    return HealthResponse(status="ok", version="1.0")
