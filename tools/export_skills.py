#!/usr/bin/env python3
"""
export_skills.py

Generates four artifacts from the skills/ directory:
  1. docs/api/skills.json              — full JSON index of all skills
  2. docs/api/skills.yaml              — YAML version of the same index
  3. docs/api/skills-schema.json       — OpenAPI-style JSON Schema
  4. docs/api/jsonld/{cat}/{id}.jsonld — JSON-LD per skill (schema.org/TechArticle)
  5. docs/api/jsonld/index.jsonld      — JSON-LD ItemList of all skills

Usage:
    python3 tools/export_skills.py
"""

import os
import re
import glob
import json
import datetime
from datetime import timezone

try:
    import yaml
except ImportError:
    yaml = None

BASE_URL = "https://samotech.github.io/skills-tree"
REPO_URL = "https://github.com/SamoTech/skills-tree"

# ---------------------------------------------------------------------------
# Time helpers
# ---------------------------------------------------------------------------

def _utc_now_iso() -> str:
    """Return the current UTC time as an ISO-8601 string with Z suffix.

    Uses datetime.now(timezone.utc) instead of the deprecated
    datetime.utcnow(), which was removed in Python 3.13.
    """
    return datetime.datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

FRONTMATTER_FIELDS = [
    ("category",     r"\*\*Category:\*\*\s*`?([^`\n]+)`?"),
    ("level",        r"\*\*Skill Level:\*\*\s*`?([^`\n]+)`?"),
    ("stability",    r"\*\*Stability:\*\*\s*`?([^`\n]+)`?"),
    ("version",      r"\*\*Version:\*\*\s*`?([^`\n]+)`?"),
    ("added",        r"\*\*Added:\*\*\s*`?([^`\n]+)`?"),
    ("last_updated", r"\*\*Last Updated:\*\*\s*`?([^`\n]+)`?"),
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

    # Description (first non-empty paragraph after frontmatter block)
    desc_m = re.search(
        r'---+\s*\n(.*?)(?=\n---)', content[content.find('\n---') + 1:], re.DOTALL
    )
    if desc_m:
        raw = desc_m.group(1).strip()
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

    # Related skills (extract link targets, dedup while preserving order)
    related_raw = re.findall(r'\[.*?\]\((\.\..*?\.md)\)', content)
    seen: set[str] = set()
    skill["related"] = [r for r in related_raw if not (r in seen or seen.add(r))]

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
    "$id": f"{BASE_URL}/api/skills-schema.json",
    "title": "Skill",
    "description": "A single AI agent skill entry in the Skills Tree index",
    "type": "object",
    "required": ["id", "name", "path"],
    "properties": {
        "id":           {"type": "string",  "description": "kebab-case filename without extension"},
        "name":         {"type": "string",  "description": "Human-readable skill title (first H1)"},
        "path":         {"type": "string",  "description": "Relative path from repo root"},
        "description":  {"type": ["string", "null"], "description": "Short description (max 400 chars)"},
        "category":     {"type": ["string", "null"]},
        "category_dir": {"type": ["string", "null"]},
        "level":        {"type": ["string", "null"], "enum": ["basic", "intermediate", "advanced", None]},
        "stability":    {"type": ["string", "null"], "enum": ["stable", "experimental", "deprecated", None]},
        "version":      {"type": ["string", "null"], "enum": ["v1", "v2", "v3", None]},
        "added":        {"type": ["string", "null"], "pattern": "^\\d{4}-\\d{2}$"},
        "last_updated": {"type": ["string", "null"], "pattern": "^\\d{4}-\\d{2}$"},
        "sections":     {"type": "array", "items": {"type": "string"}},
        "related":      {"type": "array", "items": {"type": "string"}},
    },
    "additionalProperties": False,
}


# ---------------------------------------------------------------------------
# JSON-LD helpers
# ---------------------------------------------------------------------------

# P7 FIX: corrected LEVEL_TO_ED mapping.
# Previous mapping was:
#   "intermediate": "https://schema.org/HasHealthAspect"  <- wrong (health vocab)
#   "advanced":     "https://schema.org/Expert"           <- not a schema.org IRI
# Now uses schema.org/DefinedTerm URNs recommended for educationalLevel,
# consistent with Google's structured data guidelines for educational content.
LEVEL_TO_ED = {
    "basic":        "https://schema.org/DefinedTerm",  # rendered with name="Beginner"
    "intermediate": "https://schema.org/DefinedTerm",  # rendered with name="Intermediate"
    "advanced":     "https://schema.org/DefinedTerm",  # rendered with name="Advanced"
}

# Human-readable labels for educationalLevel DefinedTerm objects
LEVEL_LABELS = {
    "basic":        "Beginner",
    "intermediate": "Intermediate",
    "advanced":     "Advanced",
}


def skill_url(skill: dict) -> str:
    """Canonical GitHub URL for the skill file."""
    return f"{REPO_URL}/blob/main/{skill['path']}"


def skill_jsonld_url(skill: dict) -> str:
    """GitHub Pages URL of this skill's JSON-LD file."""
    cat = skill.get("category_dir") or "uncategorized"
    return f"{BASE_URL}/api/jsonld/{cat}/{skill['id']}.jsonld"


def build_skill_jsonld(skill: dict) -> dict:
    """
    Build a schema.org/TechArticle JSON-LD object for a single skill.

    Vocabulary used:
      - schema:TechArticle  — best fit for a structured technical how-to document
      - schema:about        — points to schema:Thing describing the AI skill topic
      - ai-skill:*          — custom properties under the skills-tree context extension
    """
    now = _utc_now_iso()
    url = skill_url(skill)
    cat = skill.get("category_dir") or "uncategorized"

    doc = {
        "@context": [
            "https://schema.org",
            {
                "ai-skill": f"{BASE_URL}/api/context#",
                "skillId":       {"@id": "ai-skill:skillId"},
                "skillVersion":  {"@id": "ai-skill:skillVersion"},
                "skillLevel":    {"@id": "ai-skill:skillLevel"},
                "skillStability":{"@id": "ai-skill:skillStability"},
                "categoryDir":   {"@id": "ai-skill:categoryDir"},
                "sections":      {"@id": "ai-skill:sections",  "@container": "@list"},
                "relatedSkills": {"@id": "ai-skill:relatedSkills", "@container": "@list"},
                "failureModes":  {"@id": "ai-skill:failureModes"},
                "promptPatterns":{"@id": "ai-skill:promptPatterns"},
            }
        ],
        "@type": "TechArticle",
        "@id": url,
        "name": skill["name"],
        "headline": skill["name"],
        "description": skill.get("description") or "",
        "url": url,
        "isPartOf": {
            "@type": "Dataset",
            "@id": f"{BASE_URL}/api/skills.json",
            "name": "Skills Tree — AI Agent Skill Index",
            "url": BASE_URL,
        },
        "publisher": {
            "@type": "Organization",
            "name": "SamoTech",
            "url": "https://github.com/SamoTech",
        },
        "inLanguage": "en",
        "dateModified": now,
        # Custom ai-skill properties
        "skillId":       skill["id"],
        "skillVersion":  skill.get("version"),
        "skillLevel":    skill.get("level"),
        "skillStability":skill.get("stability"),
        "categoryDir":   cat,
        "sections":      skill.get("sections", []),
        "relatedSkills": skill.get("related", []),
    }

    # P7 FIX: emit educationalLevel as a schema:DefinedTerm object (not a bare
    # string). Previously emitted skill['level'].capitalize() which produced
    # e.g. "Basic" — a plain string that validators reject as not a valid
    # schema.org educationalLevel value.
    level = skill.get("level", "").lower() if skill.get("level") else ""
    if level in LEVEL_TO_ED:
        doc["educationalLevel"] = {
            "@type": "DefinedTerm",
            "name": LEVEL_LABELS[level],
            "inDefinedTermSet": "https://schema.org/EducationalOccupationalCredential",
        }

    # schema:datePublished from `added` field (YYYY-MM format)
    if skill.get("added"):
        doc["datePublished"] = skill["added"] + "-01"  # approximate day

    # schema:keywords  — derive from category_dir and id tokens
    keywords = list({
        *skill["id"].replace("-", " ").split(),
        *(cat.split("-")[1:] if cat and "-" in cat else [cat or ""]),
        "AI agent", "LLM skill", "skills tree",
    })
    doc["keywords"] = ", ".join(k for k in keywords if k)

    # schema:about — the AI skill as a named concept
    doc["about"] = {
        "@type": "Thing",
        "name": skill["name"],
        "description": f"An AI agent skill for {skill['name'].lower()}.",
    }

    return doc


def build_jsonld_index(skills: list) -> dict:
    """
    Build a schema.org/ItemList JSON-LD index over all skills.
    Used by search engines for sitelinks / rich results.
    """
    now = _utc_now_iso()
    items = [
        {
            "@type": "ListItem",
            "position": i + 1,
            "url": skill_url(s),
            "name": s["name"],
        }
        for i, s in enumerate(skills)
    ]
    return {
        "@context": "https://schema.org",
        "@type": "ItemList",
        "@id": f"{BASE_URL}/api/jsonld/index.jsonld",
        "name": "Skills Tree — Complete AI Agent Skill Index",
        "description": (
            "A comprehensive, versioned index of AI agent skills covering "
            "reasoning, memory, perception, code generation, tool use, and more."
        ),
        "url": BASE_URL,
        "numberOfItems": len(skills),
        "dateModified": now,
        "publisher": {
            "@type": "Organization",
            "name": "SamoTech",
            "url": "https://github.com/SamoTech",
        },
        "itemListElement": items,
    }


def generate_jsonld_files(skills: list) -> int:
    """Write one .jsonld file per skill + the index. Returns file count written."""
    written = 0
    jsonld_root = "docs/api/jsonld"
    os.makedirs(jsonld_root, exist_ok=True)

    for skill in skills:
        cat = skill.get("category_dir") or "uncategorized"
        out_dir = os.path.join(jsonld_root, cat)
        os.makedirs(out_dir, exist_ok=True)
        out_path = os.path.join(out_dir, f"{skill['id']}.jsonld")
        doc = build_skill_jsonld(skill)
        with open(out_path, "w", encoding="utf-8") as fh:
            json.dump(doc, fh, indent=2, ensure_ascii=False)
        written += 1

    # Write the ItemList index
    index_path = os.path.join(jsonld_root, "index.jsonld")
    index_doc = build_jsonld_index(skills)
    with open(index_path, "w", encoding="utf-8") as fh:
        json.dump(index_doc, fh, indent=2, ensure_ascii=False)
    print(f"[export] Wrote {index_path} ({len(skills)} list items)")
    written += 1

    return written


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    os.makedirs("docs/api", exist_ok=True)

    print("[export] Scanning skills/ ...")
    skills = build_index()
    print(f"[export] Found {len(skills)} skills.")

    envelope = {
        "generated": _utc_now_iso(),
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
        with open(yaml_path, "w", encoding="utf-8") as fh:
            fh.write("# Install PyYAML for full YAML export\n")
            json.dump(envelope, fh, indent=2, ensure_ascii=False)
        print(f"[export] Wrote {yaml_path} (no PyYAML — JSON fallback)")

    # 3. Schema
    schema_path = "docs/api/skills-schema.json"
    with open(schema_path, "w", encoding="utf-8") as fh:
        json.dump(SKILL_SCHEMA, fh, indent=2, ensure_ascii=False)
    print(f"[export] Wrote {schema_path}")

    # 4. JSON-LD per skill + index
    print("[export] Generating JSON-LD files ...")
    n = generate_jsonld_files(skills)
    print(f"[export] Wrote {n} JSON-LD files to docs/api/jsonld/")

    print("[export] Done.")


if __name__ == "__main__":
    main()
