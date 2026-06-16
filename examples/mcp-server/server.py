"""
Skills Tree MCP Server

Exposes Skills Tree as MCP tools for Claude Desktop, Cursor, and
any MCP-compatible AI host.

Transport: stdio (Model Context Protocol standard)

Usage:
    python server.py
"""
from __future__ import annotations

import json
import sys
from typing import Any

try:
    from skills_tree import SkillsTree
except ImportError:
    raise SystemExit("Run: pip install skills-tree")

st = SkillsTree()


def handle_search_skills(query: str, limit: int = 10) -> list[dict]:
    skills = st.search(query, limit=limit)
    return [
        {
            "id": s.id,
            "title": s.title,
            "description": s.description,
            "tier": getattr(s, "tier", None),
            "category": getattr(s, "category", None),
        }
        for s in skills
    ]


def handle_get_skill(skill_id: str) -> dict | None:
    skill = st.get(skill_id)
    if skill is None:
        return None
    return {
        "id": skill.id,
        "title": skill.title,
        "description": skill.description,
        "prerequisites": getattr(skill, "prerequisites", []),
        "tier": getattr(skill, "tier", None),
        "category": getattr(skill, "category", None),
        "code_example": getattr(skill, "code_example", None),
    }


def handle_get_prerequisites(skill_id: str) -> list[dict]:
    try:
        prereqs = st.get_prerequisites(skill_id)
        return [{"id": s.id, "title": s.title} for s in prereqs]
    except Exception:
        return []


def handle_get_category(category: str) -> list[dict]:
    try:
        skills = st.get_category(category)
        return [{"id": s.id, "title": s.title, "tier": getattr(s, "tier", None)} for s in skills]
    except Exception:
        return []


# --- Minimal stdio MCP dispatcher ---

TOOLS = [
    {
        "name": "search_skills",
        "description": "Search Skills Tree for skills matching a query. Returns top matches with ID, title, description, and tier.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "Search query"},
                "limit": {"type": "integer", "default": 10, "description": "Max results"},
            },
            "required": ["query"],
        },
    },
    {
        "name": "get_skill",
        "description": "Get full details of a skill by its ID.",
        "inputSchema": {
            "type": "object",
            "properties": {"skill_id": {"type": "string", "description": "Skill ID"}},
            "required": ["skill_id"],
        },
    },
    {
        "name": "get_prerequisites",
        "description": "Get the prerequisite skill chain for a given skill ID.",
        "inputSchema": {
            "type": "object",
            "properties": {"skill_id": {"type": "string"}},
            "required": ["skill_id"],
        },
    },
    {
        "name": "get_category",
        "description": "List all skills in a category (e.g. '01-foundations', '03-memory').",
        "inputSchema": {
            "type": "object",
            "properties": {"category": {"type": "string"}},
            "required": ["category"],
        },
    },
]


def dispatch(method: str, params: dict) -> Any:
    if method == "tools/list":
        return {"tools": TOOLS}
    if method == "tools/call":
        name = params.get("name")
        args = params.get("arguments", {})
        if name == "search_skills":
            result = handle_search_skills(**args)
        elif name == "get_skill":
            result = handle_get_skill(**args)
        elif name == "get_prerequisites":
            result = handle_get_prerequisites(**args)
        elif name == "get_category":
            result = handle_get_category(**args)
        else:
            return {"error": f"Unknown tool: {name}"}
        return {"content": [{"type": "text", "text": json.dumps(result, indent=2)}]}
    return {"error": f"Unknown method: {method}"}


def main() -> None:
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            req = json.loads(line)
            response = {
                "jsonrpc": "2.0",
                "id": req.get("id"),
                "result": dispatch(req["method"], req.get("params", {})),
            }
        except Exception as exc:
            response = {
                "jsonrpc": "2.0",
                "id": None,
                "error": {"code": -32603, "message": str(exc)},
            }
        print(json.dumps(response), flush=True)


if __name__ == "__main__":
    main()
