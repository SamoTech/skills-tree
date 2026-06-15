#!/usr/bin/env python3
"""
Architect MCP tools — Sprint C-10

Implements an MCP-compatible tool layer on top of the existing Architect API v1.
No business logic duplication: tools call the API layer using FastAPI's TestClient
for in-process execution, which reuses the existing route handlers and engine stack.
"""

from __future__ import annotations

from typing import Any, Dict, List
from fastapi.testclient import TestClient

from api.main import app

_client = TestClient(app)


class MCPToolError(RuntimeError):
    """Raised when an MCP tool invocation fails."""


def _post_json(path: str, payload: Dict[str, Any]) -> Dict[str, Any]:
    response = _client.post(path, json=payload)
    if response.status_code >= 400:
        try:
            data = response.json()
        except Exception:
            data = {"error": {"message": response.text}}
        raise MCPToolError(data.get("error", {}).get("detail") or data.get("detail") or str(data))
    return response.json()


def _get_json(path: str) -> Dict[str, Any]:
    response = _client.get(path)
    if response.status_code >= 400:
        try:
            data = response.json()
        except Exception:
            data = {"error": {"message": response.text}}
        raise MCPToolError(data.get("error", {}).get("detail") or data.get("detail") or str(data))
    return response.json()


# ---------------------------------------------------------------------------
# MCP tool implementations
# ---------------------------------------------------------------------------

def recommend_skills(goal: str, experience: str = "intermediate", time_budget_hours: int | None = None) -> Dict[str, Any]:
    """
    Get live Architect recommendations for a goal.

    Parameters
    ----------
    goal : str
        Goal name or goal ID.
    experience : str
        beginner | intermediate | advanced
    time_budget_hours : int | None
        Optional study budget filter.
    """
    payload: Dict[str, Any] = {"goal": goal, "experience": experience}
    if time_budget_hours is not None:
        payload["time_budget_hours"] = time_budget_hours
    return _post_json("/recommend", payload)


def generate_blueprint(goal: str) -> Dict[str, Any]:
    """Generate a blueprint JSON for the given goal using BlueprintGenerator."""
    return _post_json("/blueprint", {"goal": goal})


def list_goals() -> List[Dict[str, Any]]:
    """Return all taxonomy goals from GoalTaxonomyParser via the API layer."""
    return _get_json("/goals")["goals"]


def list_skills() -> List[Dict[str, Any]]:
    """Return all graph skills from SkillsGraph via the API layer."""
    return _get_json("/skills")["skills"]


# ---------------------------------------------------------------------------
# MCP manifest / tool metadata helpers
# ---------------------------------------------------------------------------

def tool_schemas() -> List[Dict[str, Any]]:
    """Return MCP-style tool contracts for registration and documentation."""
    return [
        {
            "name": "recommend_skills",
            "description": "Get live Architect skill recommendations for a goal.",
            "input_schema": {
                "type": "object",
                "properties": {
                    "goal": {"type": "string", "description": "Goal name or ID, e.g. 'Coding Agent' or 'G01'"},
                    "experience": {"type": "string", "enum": ["beginner", "intermediate", "advanced"], "default": "intermediate"},
                    "time_budget_hours": {"type": "integer", "minimum": 1},
                },
                "required": ["goal"],
            },
        },
        {
            "name": "generate_blueprint",
            "description": "Generate a full architecture blueprint JSON for a goal.",
            "input_schema": {
                "type": "object",
                "properties": {
                    "goal": {"type": "string", "description": "Goal name or ID"},
                },
                "required": ["goal"],
            },
        },
        {
            "name": "list_goals",
            "description": "List all taxonomy goals known to Architect.",
            "input_schema": {
                "type": "object",
                "properties": {},
                "required": [],
            },
        },
        {
            "name": "list_skills",
            "description": "List all graph skills known to Architect.",
            "input_schema": {
                "type": "object",
                "properties": {},
                "required": [],
            },
        },
    ]


def dispatch_tool(name: str, arguments: Dict[str, Any] | None = None) -> Any:
    """Generic dispatcher used by the MCP server wrapper and tests."""
    arguments = arguments or {}
    if name == "recommend_skills":
        return recommend_skills(**arguments)
    if name == "generate_blueprint":
        return generate_blueprint(**arguments)
    if name == "list_goals":
        return list_goals()
    if name == "list_skills":
        return list_skills()
    raise MCPToolError(f"Unknown tool: {name}")
