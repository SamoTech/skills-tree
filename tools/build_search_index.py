#!/usr/bin/env python3
"""
build_search_index.py

Builds a Lunr.js-compatible JSON search index from all skill Markdown files.
Output is written to docs/search-index.json (or the path given by --output).

The index format is a flat JSON array of document objects that the static
site's client-side Lunr.js instance can consume directly via lunr.Index.load()
or by building a fresh index from the documents array:

    [
      {
        "id":          "01-perception/image-understanding",
        "title":       "Image Understanding",
        "category":    "01-perception",
        "level":       "intermediate",
        "stability":   "stable",
        "tags":        ["vision", "multimodal"],
        "description": "Interpret and reason about visual content ...",
        "body":        "## Description\\n..."
      },
      ...
    ]

Usage:
    python tools/build_search_index.py \\
        --skills-root skills/ \\
        --output docs/search-index.json
"""

import argparse
import json
import re
import sys
from pathlib import Path

try:
    import yaml  # PyYAML — installed in CI via: pip install PyYAML==6.0.2
except ImportError:  # pragma: no cover
    print("ERROR: PyYAML is required. Run: pip install pyyaml", file=sys.stderr)
    sys.exit(1)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _parse_frontmatter(text: str) -> tuple[dict, str]:
    """Split YAML frontmatter from body.  Returns (meta_dict, body_text)."""
    if not text.startswith("---"):
        return {}, text
    end = text.find("\n---", 3)
    if end == -1:
        return {}, text
    fm_raw = text[4:end]          # between the two '---' delimiters
    body   = text[end + 4:]       # everything after the closing '---'
    try:
        meta = yaml.safe_load(fm_raw) or {}
    except yaml.YAMLError:
        meta = {}
    return meta, body


def _strip_markdown(text: str) -> str:
    """Remove common Markdown syntax so body text is plain for indexing."""
    # Remove fenced code blocks
    text = re.sub(r"```[\s\S]*?```", " ", text)
    # Remove inline code
    text = re.sub(r"`[^`]+`", " ", text)
    # Remove images
    text = re.sub(r"!\[[^\]]*\]\([^)]*\)", "", text)
    # Remove links, keep link text
    text = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", text)
    # Remove ATX headings markers
    text = re.sub(r"^#+\s+", "", text, flags=re.MULTILINE)
    # Remove bold/italic markers
    text = re.sub(r"[*_]{1,3}([^*_]+)[*_]{1,3}", r"\1", text)
    # Collapse whitespace
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def _coerce_tags(raw) -> list[str]:
    """Normalise the `tags` frontmatter field to a flat list of strings."""
    if raw is None:
        return []
    if isinstance(raw, list):
        return [str(t).strip() for t in raw if t]
    if isinstance(raw, str):
        # Handle comma-separated string: "vision, multimodal, llm"
        return [t.strip() for t in raw.split(",") if t.strip()]
    return []


# ---------------------------------------------------------------------------
# Core builder
# ---------------------------------------------------------------------------

def build_index(skills_root: Path) -> list[dict]:
    """Walk *skills_root* and return a list of search document dicts."""
    documents: list[dict] = []

    for md_file in sorted(skills_root.rglob("*.md")):
        # Skip category README files — they are navigational, not skill pages
        if md_file.name == "README.md":
            continue

        try:
            text = md_file.read_text(encoding="utf-8", errors="ignore")
        except OSError as exc:
            print(f"[WARN] Cannot read {md_file}: {exc}", file=sys.stderr)
            continue

        meta, body = _parse_frontmatter(text)

        # Build a stable, human-readable document ID:
        # e.g. "01-perception/image-understanding"
        try:
            rel = md_file.relative_to(skills_root)
        except ValueError:
            rel = md_file
        doc_id = str(rel.with_suffix("")).replace("\\", "/")

        # Derive category slug from the first path component
        category = rel.parts[0] if len(rel.parts) > 1 else ""

        doc = {
            "id":          doc_id,
            "title":       str(meta.get("title", "")).strip('"'),
            "category":    str(meta.get("category", category)),
            "level":       str(meta.get("level",    "intermediate")),
            "stability":   str(meta.get("stability", "stable")),
            "tags":        _coerce_tags(meta.get("tags")),
            "description": str(meta.get("description", "")).strip('"'),
            "body":        _strip_markdown(body),
        }
        documents.append(doc)

    return documents


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Build a Lunr.js-compatible JSON search index from skill Markdown files."
    )
    parser.add_argument(
        "--skills-root",
        default="skills",
        help="Root directory containing skill .md files (default: skills)",
    )
    parser.add_argument(
        "--output",
        default="docs/search-index.json",
        help="Destination path for the generated JSON index (default: docs/search-index.json)",
    )
    args = parser.parse_args()

    skills_root = Path(args.skills_root)
    if not skills_root.exists():
        print(f"ERROR: skills root '{skills_root}' does not exist.", file=sys.stderr)
        sys.exit(1)

    print(f"Building search index from '{skills_root}'...")
    documents = build_index(skills_root)

    if not documents:
        print("WARNING: No skill documents found — index will be empty.", file=sys.stderr)

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(documents, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    print(f"Done. {len(documents)} document(s) written to '{output_path}'.")


if __name__ == "__main__":
    main()
