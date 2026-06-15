#!/usr/bin/env python3
"""
Pydantic request / response models for Architect API v1.
All business logic lives in tools/architect.py — these are pure schema contracts.
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field, field_validator


# ---------------------------------------------------------------------------
# Shared / primitive models
# ---------------------------------------------------------------------------

class SkillSummary(BaseModel):
    id: str = Field(..., description="Canonical skill ID (e.g. 'skill:rag-retrieval')")
    name: str = Field(..., description="Human-readable skill name")
    rank: Optional[int] = Field(None, description="Rank within this recommendation set")
    score: Optional[float] = Field(None, description="Composite numeric score")
    confidence: Optional[float] = Field(None, ge=0.0, le=1.0, description="Evidence-derived confidence [0,1]")
    priority: Optional[str] = Field(None, description="Taxonomy priority: critical | high | medium | low")
    learn_time: Optional[str] = Field(None, description="Estimated learning time (e.g. '8 hours')")
    explanation: Optional[List[str]] = Field(default_factory=list)
    evidence: Optional[Dict[str, Any]] = Field(default_factory=dict)
    score_breakdown: Optional[Dict[str, float]] = Field(default_factory=dict)
    stability: Optional[str] = None


class GoalSummary(BaseModel):
    id: str = Field(..., description="Goal ID (e.g. 'G01')")
    name: str
    description: Optional[str] = None
    difficulty: Optional[str] = None
    skills_count: Optional[int] = None


class SkillNode(BaseModel):
    id: str
    name: str
    category: Optional[str] = None
    stability: Optional[str] = None
    description: Optional[str] = None
    tags: Optional[List[str]] = Field(default_factory=list)


# ---------------------------------------------------------------------------
# GET /health
# ---------------------------------------------------------------------------

class HealthResponse(BaseModel):
    status: str = "ok"
    version: str = "1.0"


# ---------------------------------------------------------------------------
# GET /goals
# ---------------------------------------------------------------------------

class GoalsResponse(BaseModel):
    total: int
    goals: List[GoalSummary]


# ---------------------------------------------------------------------------
# GET /skills
# ---------------------------------------------------------------------------

class SkillsResponse(BaseModel):
    total: int
    skills: List[SkillNode]


# ---------------------------------------------------------------------------
# POST /recommend
# ---------------------------------------------------------------------------

EXPERIENCE_LEVELS = {"beginner", "intermediate", "advanced"}


class RecommendRequest(BaseModel):
    goal: str = Field(..., min_length=2, max_length=200, description="Goal name or ID to resolve")
    experience: str = Field("intermediate", description="beginner | intermediate | advanced")
    time_budget_hours: Optional[int] = Field(None, ge=1, le=10000, description="Available study hours")

    @field_validator("experience")
    @classmethod
    def validate_experience(cls, v: str) -> str:
        if v.lower() not in EXPERIENCE_LEVELS:
            raise ValueError(f"experience must be one of {sorted(EXPERIENCE_LEVELS)}")
        return v.lower()


class RecommendResponse(BaseModel):
    goal: str
    goal_id: str
    confidence_score: float = Field(..., ge=0.0, le=1.0)
    required_skills: List[SkillSummary]
    optional_skills: List[SkillSummary]
    learning_path: List[str]
    deployment: Optional[str] = None
    complexity: Optional[str] = None
    estimated_learn_hours: Optional[int] = None
    calibration_applied: bool = True


# ---------------------------------------------------------------------------
# POST /blueprint
# ---------------------------------------------------------------------------

class BlueprintRequest(BaseModel):
    goal: str = Field(..., min_length=2, max_length=200, description="Goal name or ID")


# BlueprintResponse is loosely typed — BlueprintGenerator produces rich nested JSON
class BlueprintResponse(BaseModel):
    model_config = {"extra": "allow"}

    id: str
    title: str
    goal: str
    goal_id: str
    confidence_score: float
    architecture_type: str
    deployment_type: Optional[str] = None
    complexity: Optional[str] = None
    maturity: Optional[str] = None
    estimated_learn_hours: Optional[int] = None
    recommended_framework: Optional[str] = None
    required_skills: List[Dict[str, Any]] = Field(default_factory=list)
    optional_skills: List[Dict[str, Any]] = Field(default_factory=list)
    learning_path: List[str] = Field(default_factory=list)
    risks: List[Dict[str, Any]] = Field(default_factory=list)


# ---------------------------------------------------------------------------
# Error models
# ---------------------------------------------------------------------------

class ErrorDetail(BaseModel):
    code: str
    message: str
    detail: Optional[str] = None


class ErrorResponse(BaseModel):
    error: ErrorDetail
