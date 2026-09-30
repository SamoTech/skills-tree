#!/usr/bin/env python3
"""Validate standards-compatible Agent Skills packages and their evidence gate."""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / "agent-skills"
NAME_RE = re.compile(r"^[a-z0-9](?:[a-z0-9-]{0,62}[a-z0-9])?$")
SECRET_RE = re.compile(r"(?i)(api[_-]?key|secret|password|token)\s*[:=]\s*['\"][^'\"]+['\"]")

def parse_frontmatter(text: str) -> dict[str, str]:
    if not text.startswith("---\n"):
        return {}
    end = text.find("\n---\n", 4)
    if end < 0:
        return {}
    data: dict[str, str] = {}
    for line in text[4:end].splitlines():
        if ":" not in line or line.startswith((" ", "\t", "-")):
            continue
        key, value = line.split(":", 1)
        data[key.strip()] = value.strip().strip('"').strip("'")
    return data

def validate(path: Path) -> list[str]:
    errors: list[str] = []
    fm = parse_frontmatter(path.read_text(encoding="utf-8"))
    expected = path.parent.name
    name = fm.get("name", "")
    description = fm.get("description", "")
    if not name:
        errors.append("missing name")
    elif name != expected:
        errors.append(f"name {name!r} does not match directory {expected!r}")
    elif not NAME_RE.fullmatch(name):
        errors.append("name is not lowercase kebab-case (1-64 chars)")
    if not description:
        errors.append("missing description")
    elif len(description) > 1024:
        errors.append("description exceeds 1024 characters")
    body = path.read_text(encoding="utf-8")
    if "## Evidence" not in body:
        errors.append("missing Evidence section")
    if "Evidence status:" not in body:
        errors.append("missing evidence status")
    if SECRET_RE.search(body):
        errors.append("possible hard-coded secret")
    if len(body.splitlines()) > 500:
        errors.append("SKILL.md exceeds recommended 500-line body budget")
    return errors

def main() -> int:
    files = sorted(ROOT.glob("*/SKILL.md"))
    if not files:
        print("No Agent Skills packages found.")
        return 1
    failures = 0
    for path in files:
        errors = validate(path)
        if errors:
            failures += 1
            print(f"FAIL {path}:")
            for error in errors:
                print(f"  - {error}")
        else:
            print(f"OK   {path}")
    print(f"Validated {len(files)} skill package(s); {failures} failed.")
    return 1 if failures else 0

if __name__ == "__main__":
    raise SystemExit(main())
