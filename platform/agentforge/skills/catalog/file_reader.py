"""Skill: file_reader — read local files (text, JSON, CSV, PDF)."""
from __future__ import annotations
import json
import csv
import io
from pathlib import Path
from agentforge.skills.base import BaseSkill, SkillInput, SkillOutput


class FileReaderSkill(BaseSkill):
    name = "file_reader"
    description = "Read the contents of a local file. Supports .txt, .json, .csv, .md, .py."
    category = "filesystem"
    tags = ["file", "read", "text", "json", "csv", "markdown"]
    level = "basic"
    input_schema = {
        "path": {"type": "string", "required": True, "description": "Absolute or relative file path"},
        "encoding": {"type": "string", "default": "utf-8"},
        "max_bytes": {"type": "integer", "default": 1_000_000},
    }
    output_schema = {
        "content": {"type": "string"},
        "parsed": {"type": "any"},
        "size_bytes": {"type": "integer"},
        "extension": {"type": "string"},
    }

    async def execute(self, inp: SkillInput) -> SkillOutput:
        file_path = Path(inp.data.get("path", ""))
        encoding = inp.data.get("encoding", "utf-8")
        max_bytes = int(inp.data.get("max_bytes", 1_000_000))

        if not file_path.exists():
            return SkillOutput(success=False, error=f"File not found: {file_path}")

        ext = file_path.suffix.lower()
        raw = file_path.read_bytes()[:max_bytes]
        content = raw.decode(encoding, errors="replace")
        parsed = None

        if ext == ".json":
            try:
                parsed = json.loads(content)
            except json.JSONDecodeError:
                pass
        elif ext == ".csv":
            try:
                reader = csv.DictReader(io.StringIO(content))
                parsed = list(reader)
            except Exception:
                pass

        return SkillOutput(
            success=True,
            data={
                "content": content,
                "parsed": parsed,
                "size_bytes": len(raw),
                "extension": ext,
            },
        )
