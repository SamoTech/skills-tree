#!/usr/bin/env python3
"""
export_skills.py

Generates three artifacts from the skills/ directory:
  1. docs/api/skills.json        — full JSON index of all skills
  2. docs/api/skills.yaml        — YAML version of the same index
  3. docs/api/skills-schema.json — OpenAPI-style JSON Schema describing a skill object

Usage:
    python3 tools/export_skills.py

Outputs are written to docs/api/ (created if absent).
"""

import os
import re
import glob
import json
import datetime

try:
    import yaml
except ImportError:
    yaml = None

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

FRONTMATTER_FIELDS = [
    ("category",    r"\*\*Category:\*\*\s*`?([^`\n]+)`?"),
    ("level",       r"\*\*Skill Level:\*\*\s*`?([^`\n]+)`?"),
    ("stability",   r"\*\*Stability:\*\*\s*`?([^`\n]+)`?"),
    ("version",     r"\*\*Version:\*\*\s*`?([^`\n]+)`?"),
    ("added",       r"\*\*Added:\*\*\s*`?([^`\n]+)`?"),
    ("last_updated",r"\*\*Last Updated:\*\*\s*`?([^`\n]+)`?"),
]


def parse_skill(filepath: str) -> dict:
    """Extract metadata from a single skill markdown file."""
    with open(filepath, encoding="utf-8") as fh:
        content = fh.read()

    skill: dict = {
        "id": os.path.splitext(os.path.basename(filepath))[0],
        "path": filepath.replace("\\", "/"),
    }

    # Title (first H1)
    m = re.search(r'^# (.+)$', content, re.MULTILINE)
    skill["name"] = m.group(1).strip() if m else skill["id"]

    # Description (first non-empty paragraph after frontmatter block, before first ---)
    desc_m = re.search(
        r'---+\s*\n(.*?)(?=\n---)', content[content.find('\n---')+1:], re.DOTALL
    )
    if desc_m:
        raw = desc_m.group(1).strip()
        # Take first real sentence / paragraph
        para = re.split(r'\n\n', raw)[0].strip()
        skill["description"] = para[:400] if para else ""
    else:
        skill["description"] = ""

    # Frontmatter fields
    for key, pattern in FRONTMATTER_FIELDS:
        m = re.search(pattern, content, re.IGNORECASE)
        skill[key] = m.group(1).strip().strip('`') if m else None

    # Sections present
    sections = re.findall(r'^## (.+)$', content, re.MULTILINE)
    skill["sections"] = sections

    # Related skills (extract link targets)
    related = re.findall(r'\[.*?\]\((\.\..*?\.md)\)', content)
    skill["related"] = related

    # Tags derived from category path
    parts = filepath.replace("\\", "/").split("/")
    skill["category_dir"] = parts[1] if len(parts) > 2 else None

    return skill


def build_index() -> list:
    """Walk skills/** and return a sorted list of skill dicts."""
    skills = []
    for filepath in sorted(glob.glob("skills/**/*.md", recursive=True)):
        try:
            skills.append(parse_skill(filepath))
        except Exception as exc:  # noqa: BLE001
            print(f"[export] WARNING: could not parse {filepath}: {exc}")
    return skills


# ---------------------------------------------------------------------------
# OpenAPI-style JSON Schema
# ---------------------------------------------------------------------------

SKILL_SCHEMA = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "$id": "https://samotech.github.io/skills-tree/api/skills-schema.json",
    "title": "Skill",
    "description": "A single AI agent skill entry in the Skills Tree index",
    "type": "object",
    "required": ["id", "name", "path"],
    "properties": {
        "id":          {"type": "string",  "description": "kebab-case filename without extension"},
        "name":        {"type": "string",  "description": "Human-readable skill title (first H1)"},
        "path":        {"type": "string",  "description": "Relative path from repo root"},
        "description": {"type": ["string", "null"], "description": "Short description (max 400 chars)"},
        "category":    {"type": ["string", "null"], "description": "Skill category slug from frontmatter"},
        "category_dir":{"type": ["string", "null"], "description": "Top-level category directory (e.g. 01-perception)"},
        "level":       {"type": ["string", "null"], "enum": ["basic", "intermediate", "advanced", None]},
        "stability":   {"type": ["string", "null"], "enum": ["stable", "experimental", "deprecated", None]},
        "version":     {"type": ["string", "null"], "enum": ["v1", "v2", "v3", None]},
        "added":       {"type": ["string", "null"], "pattern": "^\\d{4}-\\d{2}$"},
        "last_updated":{"type": ["string", "null"], "pattern": "^\\d{4}-\\d{2}$"},
        "sections":    {"type": "array",   "items": {"type": "string"}, "description": "H2 section headings present in the file"},
        "related":     {"type": "array",   "items": {"type": "string"}, "description": "Relative paths of related skill files"},
    },
    "additionalProperties": False,
}


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    os.makedirs("docs/api", exist_ok=True)

    print("[export] Scanning skills/ ...")
    skills = build_index()
    print(f"[export] Found {len(skills)} skills.")

    envelope = {
        "generated": datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
        "count": len(skills),
        "skills": skills,
    }

    # 1. JSON
    json_path = "docs/api/skills.json"
    with open(json_path, "w", encoding="utf-8") as fh:
        json.dump(envelope, fh, indent=2, ensure_ascii=False)
    print(f"[export] Wrote {json_path} ({os.path.getsize(json_path):,} bytes)")

    # 2. YAML
    yaml_path = "docs/api/skills.yaml"
    if yaml:
        with open(yaml_path, "w", encoding="utf-8") as fh:
            yaml.dump(envelope, fh, allow_unicode=True, sort_keys=False)
        print(f"[export] Wrote {yaml_path}")
    else:
        # Minimal YAML-ish output without PyYAML
        with open(yaml_path, "w", encoding="utf-8") as fh:
            fh.write(f"# Install PyYAML (pip install pyyaml) for full YAML export\n")
            fh.write(f"# Falling back to JSON-formatted YAML\n")
            json.dump(envelope, fh, indent=2, ensure_ascii=False)
        print(f"[export] Wrote {yaml_path} (no PyYAML — JSON fallback)")

    # 3. Schema
    schema_path = "docs/api/skills-schema.json"
    with open(schema_path, "w", encoding="utf-8") as fh:
        json.dump(SKILL_SCHEMA, fh, indent=2, ensure_ascii=False)
    print(f"[export] Wrote {schema_path}")

    print("[export] Done.")


if __name__ == "__main__":
    main()
