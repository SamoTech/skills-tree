#!/usr/bin/env python3
"""
Architect API v1 — Sprint C-09

FastAPI application exposing the Skills Tree Architect engine as a
consumable HTTP service.

Endpoints
---------
GET  /health        — liveness probe
GET  /goals         — list all taxonomy goals
GET  /skills        — list all graph skill nodes
POST /recommend     — calibrated skill recommendations
POST /blueprint     — full architecture blueprint

Docs
----
OpenAPI JSON : /openapi.json
Swagger UI   : /docs
ReDoc        : /redoc

Usage
-----
    uvicorn api.main:app --reload
    # or from repo root:
    python -m uvicorn api.main:app --host 0.0.0.0 --port 8000
"""

from __future__ import annotations

import logging
import os

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from api.routes import health, goals, skills, recommend, blueprint
from api.models import ErrorResponse, ErrorDetail

logger = logging.getLogger("api.main")

# ---------------------------------------------------------------------------
# App instance
# ---------------------------------------------------------------------------

app = FastAPI(
    title="Skills Tree Architect API",
    description=(
        "Taxonomy-driven skill recommendation engine for AI agent builders. "
        "Powered by GoalTaxonomyParser, SkillsGraph, RecommendationEngine, "
        "RankingCalibrator (C-08), and BlueprintGenerator."
    ),
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    contact={
        "name":  "SamoTech",
        "url":   "https://github.com/SamoTech/skills-tree",
    },
    license_info={
        "name": "MIT",
        "url":  "https://github.com/SamoTech/skills-tree/blob/main/LICENSE",
    },
)

# ---------------------------------------------------------------------------
# CORS
# ---------------------------------------------------------------------------

def _cors_policy() -> tuple[list[str], str | None]:
    """Resolve the CORS policy from the environment.

    SKILLS_TREE_API_CORS_ORIGINS accepts a comma-separated list of allowed
    origins, or "*" to explicitly restore the previous wildcard policy.
    When unset, only local development origins (localhost / 127.0.0.1 on
    any port) are allowed, matching the documented local-server usage.
    (Audit finding AUD-011.)
    """
    raw = os.getenv("SKILLS_TREE_API_CORS_ORIGINS", "").strip()
    if raw == "*":
        return ["*"], None
    if raw:
        origins = [origin.strip() for origin in raw.split(",") if origin.strip()]
        return origins, None
    return [], r"^https?://(localhost|127\.0\.0\.1)(:\d+)?$"


_origins, _origin_regex = _cors_policy()

app.add_middleware(
    CORSMiddleware,
    allow_origins=_origins,
    allow_origin_regex=_origin_regex,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["Content-Type", "Accept"],
)

# ---------------------------------------------------------------------------
# Global error handlers
# ---------------------------------------------------------------------------

@app.exception_handler(404)
async def not_found_handler(request: Request, exc):
    return JSONResponse(
        status_code=404,
        content=ErrorResponse(
            error=ErrorDetail(code="NOT_FOUND", message="Resource not found", detail=str(exc))
        ).model_dump(),
    )


@app.exception_handler(422)
async def validation_error_handler(request: Request, exc):
    return JSONResponse(
        status_code=422,
        content=ErrorResponse(
            error=ErrorDetail(
                code="VALIDATION_ERROR",
                message="Request validation failed",
                detail=str(exc),
            )
        ).model_dump(),
    )


@app.exception_handler(500)
async def internal_error_handler(request: Request, exc):
    # Log the real exception server-side (audit finding AUD-011); never
    # disclose server internals to clients.
    logger.exception("Unhandled server error on %s %s", request.method, request.url.path)
    return JSONResponse(
        status_code=500,
        content=ErrorResponse(
            error=ErrorDetail(
                code="INTERNAL_ERROR",
                message="Internal server error",
                detail="An unexpected error occurred. Server-side details are logged, not disclosed.",
            )
        ).model_dump(),
    )


# ---------------------------------------------------------------------------
# Routers
# ---------------------------------------------------------------------------

app.include_router(health.router)
app.include_router(goals.router)
app.include_router(skills.router)
app.include_router(recommend.router)
app.include_router(blueprint.router)


# ---------------------------------------------------------------------------
# Root redirect
# ---------------------------------------------------------------------------

@app.get("/", include_in_schema=False)
async def root():
    return {
        "service": "Skills Tree Architect API",
        "version": "1.0.0",
        "docs":    "/docs",
        "openapi": "/openapi.json",
        "redoc":   "/redoc",
    }
