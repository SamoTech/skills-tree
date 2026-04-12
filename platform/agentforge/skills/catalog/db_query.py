"""Skill: db_query — run read-only SQL queries against a database."""
from __future__ import annotations
import asyncio
from agentforge.skills.base import BaseSkill, SkillInput, SkillOutput


class DbQuerySkill(BaseSkill):
    name = "db_query"
    description = "Execute a read-only SQL SELECT query and return results as a list of dicts."
    category = "data"
    tags = ["sql", "database", "postgres", "sqlite", "query", "analytics"]
    level = "intermediate"
    input_schema = {
        "query": {"type": "string", "required": True, "description": "SQL SELECT query"},
        "dsn": {"type": "string", "description": "Database connection string (overrides env)"},
        "limit": {"type": "integer", "default": 100},
    }
    output_schema = {
        "rows": {"type": "array"},
        "row_count": {"type": "integer"},
        "columns": {"type": "array"},
    }

    async def execute(self, inp: SkillInput) -> SkillOutput:
        query = inp.data.get("query", "").strip()
        limit = int(inp.data.get("limit", 100))

        if not query:
            return SkillOutput(success=False, error="query is required")

        # Safety: only allow SELECT
        if not query.upper().lstrip().startswith("SELECT"):
            return SkillOutput(success=False, error="Only SELECT queries are allowed")

        # Append LIMIT if not present
        if "LIMIT" not in query.upper():
            query = f"{query} LIMIT {limit}"

        try:
            import asyncpg
            from agentforge.core.config import settings
            dsn = inp.data.get("dsn") or settings.database_url.replace("+asyncpg", "")
            conn = await asyncpg.connect(dsn)
            try:
                records = await conn.fetch(query)
                rows = [dict(r) for r in records]
                columns = list(rows[0].keys()) if rows else []
            finally:
                await conn.close()

            return SkillOutput(
                success=True,
                data={"rows": rows, "row_count": len(rows), "columns": columns},
            )
        except Exception as e:
            return SkillOutput(success=False, error=str(e))
