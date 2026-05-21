#!/usr/bin/env python3
"""
build_search_index.py

Builds a Lunr.js-compatible JSON search index from all skill Markdown files.
Called by .github/workflows/generate-search-index.yml on push to main.

Output format: docs/search-index.json

The index is an array of document objects:
  [
    {
      "id":          "react",                         # skill file stem
      "key":         "09-agentic-patterns/react",     # badge key / URL slug
      "title":       "ReAct",
      "category":    "09-agentic-patterns",
      "level":       "intermediate",
      "stability":   "stable",
      "version":     "v3",
      "description": "...",
      "tags":        ["reasoning", "tool-use"],       # from related_skills slugs
      "body":        "...first 500 chars of body..."
    },
    ...
  ]

The docs/ static site loads this file and runs lunr() client-side.

Usage:
    python tools/build_search_index.py \\
        --skills-root skills/ \\
        --output docs/search-index.json
"""

import json
import re
import sys
import argparse
from pathlib import Path
from datetime import datetime, timezone

try:
    import yaml
except ImportError:
    print("PyYAML required: pip install PyYAML", file=sys.stderr)
    sys.exit(1)


# ---- Frontmatter parsing -------------------------------------------------

def _parse_frontmatter(text: str) -> tuple[dict, str]:
    """
    Split a Markdown file into (frontmatter_dict, body_text).
    Returns ({}, full_text) if no frontmatter block is found.
    """
    m = re.match(r'^---\s*\n(.*?)\n---\s*\n?(.*)', text, re.DOTALL)
    if not m:
        return {}, text
    try:
        fm = yaml.safe_load(m.group(1))
        fm = fm if isinstance(fm, dict) else {}
    except yaml.YAMLError:
        fm = {}
    return fm, m.group(2)


# ---- Body text extraction ------------------------------------------------

def _clean_body(body: str, max_chars: int = 500) -> str:
    """Strip Markdown syntax and return plain-text excerpt for search indexing."""
    # Remove code fences
    body = re.sub(r'```[\s\S]*?```', ' ', body)
    # Remove inline code
    body = re.sub(r'`[^`]+`', ' ', body)
    # Remove Markdown headings, links, emphasis
    body = re.sub(r'^#{1,6}\s+', '', body, flags=re.MULTILINE)
    body = re.sub(r'!?\[([^\]]*)\]\([^)]*\)', r'\1', body)
    body = re.sub(r'[*_]{1,3}([^*_]+)[*_]{1,3}', r'\1', body)
    # Collapse whitespace
    body = re.sub(r'\s+', ' ', body).strip()
    return body[:max_chars]


# ---- Tag extraction from related_skills ---------------------------------

def _extract_tags(fm: dict) -> list[str]:
    """Derive searchable tags from related_skills paths."""
    tags = []
    for rel in fm.get("related_skills", []):
        slug = Path(rel).stem.replace("-", " ").replace("_", " ")
        tags.append(slug)
    return tags


# ---- Main ----------------------------------------------------------------

def build_index(skills_root: Path) -> list[dict]:
    """Walk skills/ and return a list of index document dicts."""
    docs = []
    for md_path in sorted(skills_root.rglob("*.md")):
        if md_path.name.lower() == "readme.md":
            continue
        try:
            text = md_path.read_text(encoding="utf-8", errors="ignore")
            fm, body = _parse_frontmatter(text)

            # Derive category from directory structure
            parts = md_path.parts
            # parts = ('skills', '09-agentic-patterns', 'react.md')
            category = parts[1] if len(parts) > 2 else "unknown"

            # Badge key: category/stem
            key = f"{category}/{md_path.stem}"

            # Title: prefer frontmatter, fall back to first H1
            title = fm.get("title") or ""
            if not title:
                h1 = re.search(r'^#\s+(.+)$', body, re.MULTILINE)
                title = h1.group(1).strip() if h1 else md_path.stem

            docs.append({
                "id":          md_path.stem,
                "key":         key,
                "title":       title,
                "category":    category,
                "level":       fm.get("level", ""),
                "stability":   fm.get("stability", ""),
                "status":      fm.get("status", ""),
                "version":     fm.get("version", "v1"),
                "description": fm.get("description", ""),
                "tags":        _extract_tags(fm),
                "body":        _clean_body(body),
            })
        except Exception as exc:
            print(f"[search_index] WARNING: skipping {md_path}: {exc}", file=sys.stderr)

    return docs


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Build Lunr.js search index for Skills Tree static site."
    )
    parser.add_argument("--skills-root", default="skills/",
                        help="Root directory containing skill .md files")
    parser.add_argument("--output", default="docs/search-index.json",
                        help="Output path for the JSON search index")
    args = parser.parse_args()

    skills_root = Path(args.skills_root)
    if not skills_root.exists():
        print(f"ERROR: skills root '{skills_root}' not found.", file=sys.stderr)
        return 1

    print(f"[search_index] Building search index from {skills_root}...")
    docs = build_index(skills_root)
    print(f"[search_index] Indexed {len(docs)} skill documents.")

    out_path = Path(args.output)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    payload = {
        "generated": datetime.now(timezone.utc).isoformat(),
        "count": len(docs),
        "docs": docs,
    }
    out_path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"[search_index] Wrote {out_path} ({out_path.stat().st_size:,} bytes)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
