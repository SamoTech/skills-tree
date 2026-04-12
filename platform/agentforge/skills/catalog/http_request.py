"""Skill: http_request — make HTTP calls with retries and response parsing."""
from __future__ import annotations
import httpx
from tenacity import retry, stop_after_attempt, wait_exponential
from agentforge.skills.base import BaseSkill, SkillInput, SkillOutput


class HttpRequestSkill(BaseSkill):
    name = "http_request"
    description = "Make HTTP GET/POST/PUT/DELETE requests and return parsed response."
    category = "web"
    tags = ["http", "api", "rest", "webhook", "fetch"]
    level = "basic"
    input_schema = {
        "url": {"type": "string", "required": True},
        "method": {"type": "string", "default": "GET", "enum": ["GET","POST","PUT","DELETE","PATCH"]},
        "headers": {"type": "object", "default": {}},
        "body": {"type": "object", "default": None},
        "timeout": {"type": "integer", "default": 30},
    }
    output_schema = {
        "status_code": {"type": "integer"},
        "body": {"type": "any"},
        "headers": {"type": "object"},
    }

    async def execute(self, inp: SkillInput) -> SkillOutput:
        url = inp.data.get("url", "")
        method = inp.data.get("method", "GET").upper()
        headers = inp.data.get("headers", {})
        body = inp.data.get("body", None)
        timeout = int(inp.data.get("timeout", 30))

        if not url:
            return SkillOutput(success=False, error="url is required")

        try:
            async with httpx.AsyncClient(timeout=timeout) as client:
                req = client.request(
                    method, url, headers=headers,
                    json=body if isinstance(body, dict) else None,
                    content=body if isinstance(body, str) else None,
                )
                response = await req

            try:
                parsed_body = response.json()
            except Exception:
                parsed_body = response.text

            return SkillOutput(
                success=200 <= response.status_code < 300,
                data={
                    "status_code": response.status_code,
                    "body": parsed_body,
                    "headers": dict(response.headers),
                },
            )
        except Exception as e:
            return SkillOutput(success=False, error=str(e))
