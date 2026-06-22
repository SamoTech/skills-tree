#!/usr/bin/env python3
"""
tools/extract_edges.py — INITIATIVE-001 Phase D

Edge extraction engine for skills-tree.
Replaces manual R-03/R-05 missions.

Extraction sources (in order of priority):
  1. ## Related Skills sections — markdown links
  2. Explicit prerequisite language in frontmatter (dependencies field)
  3. Inline prerequisite keywords in body text

Allowed edge types:
  REQUIRES      — prerequisite, depends on, requires, before learning, foundation skill
  SUPPORTS      — supports, enables, extends, powers, executes, builds on
  RELATED_TO    — listed in Related Skills without dependency language
  SUBSKILL_OF   — explicit subskill declaration
  ALTERNATIVE_TO — listed as alternative

Usage:
  python tools/extract_edges.py                       # all categories
  python tools/extract_edges.py --category 02-reasoning
  python tools/extract_edges.py --output edges.json
  python tools/extract_edges.py --format markdown     # human-readable registry

Output:
  JSON array of edge objects conforming to schema/edge.schema.json
"""

import argparse
import json
import re
import sys
from pathlib import Path
from datetime import datetime, timezone

REPO_ROOT = Path(__file__).parent.parent
SKILLS_DIR = REPO_ROOT / "skills"

# ---------------------------------------------------------------------------
# Trigger patterns
# ---------------------------------------------------------------------------
REQUIRES_PATTERNS = [
    re.compile(r"\bprerequisite\b", re.IGNORECASE),
    re.compile(r"\bdepends on\b", re.IGNORECASE),
    re.compile(r"\brequires\b", re.IGNORECASE),
    re.compile(r"\bbefore learning\b", re.IGNORECASE),
    re.compile(r"\bfoundation skill\b", re.IGNORECASE),
]

SUPPORTS_PATTERNS = [
    re.compile(r"\bsupports\b", re.IGNORECASE),
    re.compile(r"\benables\b", re.IGNORECASE),
    re.compile(r"\bextends\b", re.IGNORECASE),
    re.compile(r"\bpowers\b", re.IGNORECASE),
    re.compile(r"\bexecutes\b", re.IGNORECASE),
    re.compile(r"\bbuilds on\b", re.IGNORECASE),
]

ALTERNATIVE_PATTERNS = [
    re.compile(r"\balternative to\b", re.IGNORECASE),
    re.compile(r"\binstead of\b", re.IGNORECASE),
    re.compile(r"\bsimilar to\b", re.IGNORECASE),
]

SUBSKILL_PATTERNS = [
    re.compile(r"\bsubskill of\b", re.IGNORECASE),
    re.compile(r"\bspecialization of\b", re.IGNORECASE),
    re.compile(r"\bpart of\b", re.IGNORECASE),
]

RELATED_SECTION_RE = re.compile(
    r"##\s+Related Skills?\s*\n(.*?)(?=\n##|\Z)", re.DOTALL | re.IGNORECASE
)
MD_LINK_RE = re.compile(r"\[([^\]]+)\]\(([^)#]+\.md)(?:#[^)]*)?\)")


# ---------------------------------------------------------------------------
# Edge type classifier
# ---------------------------------------------------------------------------
def classify_edge_type(context: str) -> tuple[str, str]:
    """Return (edge_type, confidence) based on context text."""
    for pat in REQUIRES_PATTERNS:
        if pat.search(context):
            return "REQUIRES", "high"
    for pat in SUPPORTS_PATTERNS:
        if pat.search(context):
            return "SUPPORTS", "high"
    for pat in ALTERNATIVE_PATTERNS:
        if pat.search(context):
            return "ALTERNATIVE_TO", "high"
    for pat in SUBSKILL_PATTERNS:
        if pat.search(context):
            return "SUBSKILL_OF", "high"
    return "RELATED_TO", "high"


# ---------------------------------------------------------------------------
# Target ID resolver
# ---------------------------------------------------------------------------
def resolve_target_id(href: str, source_category: str) -> str | None:
    """Resolve a markdown link href to a canonical skill ID."""
    # Strip query/fragment
    href = href.split("#")[0].strip()
    if not href.endswith(".md"):
        return None

    if href.startswith("../"):
        # Cross-category: ../09-agentic-patterns/plan-and-execute.md
        clean = href.lstrip("../")
        parts = clean.split("/")
        if len(parts) == 2:
            return f"{parts[0]}/{parts[1][:-3]}"  # strip .md
        return None
    else:
        # Same-category: causal.md or subdir/causal.md
        slug = Path(href).stem
        return f"{source_category}/{slug}"


# ---------------------------------------------------------------------------
# Per-file extractor
# ---------------------------------------------------------------------------
def extract_from_file(md_path: Path) -> list[dict]:
    """Extract all edges from a single skill markdown file."""
    edges = []
    category = md_path.parent.name
    source_id = f"{category}/{md_path.stem}"
    rel_path = str(md_path.relative_to(REPO_ROOT))

    try:
        text = md_path.read_text(encoding="utf-8")
    except Exception as e:
        print(f"  [WARN] Cannot read {md_path}: {e}", file=sys.stderr)
        return []

    # Find Related Skills section
    section_match = RELATED_SECTION_RE.search(text)
    if not section_match:
        return []

    section = section_match.group(1)
    seen = set()

    for link_match in MD_LINK_RE.finditer(section):
        link_text = link_match.group(1)
        href = link_match.group(2)
        evidence = link_match.group(0)

        # Get surrounding context line for classification
        line_start = section.rfind("\n", 0, link_match.start()) + 1
        line_end = section.find("\n", link_match.end())
        context_line = section[line_start:line_end if line_end != -1 else len(section)]
        full_context = context_line + " " + link_text

        target_id = resolve_target_id(href, category)
        if target_id is None:
            continue

        # Skip self-loops
        if target_id == source_id:
            continue

        # Dedup within file
        edge_key = (source_id, target_id)
        if edge_key in seen:
            continue
        seen.add(edge_key)

        edge_type, confidence = classify_edge_type(full_context)

        edges.append({
            "source": source_id,
            "target": target_id,
            "type": edge_type,
            "evidence": evidence.strip(),
            "source_file": rel_path,
            "confidence": confidence,
        })

    return edges


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(description="Extract edges from skill markdown files.")
    parser.add_argument("--category", help="Scan only this category (e.g. 02-reasoning).")
    parser.add_argument("--output", default="-", help="Output file path (- for stdout).")
    parser.add_argument("--format", choices=["json", "markdown"], default="json")
    args = parser.parse_args()

    all_edges = []
    categories = []

    if args.category:
        cat_dir = SKILLS_DIR / args.category
        if not cat_dir.is_dir():
            print(f"ERROR: Category directory not found: {cat_dir}", file=sys.stderr)
            sys.exit(1)
        categories = [cat_dir]
    else:
        categories = sorted(
            d for d in SKILLS_DIR.iterdir()
            if d.is_dir() and re.match(r"^[0-9]{2}-", d.name)
        )

    for cat_dir in categories:
        for md_file in sorted(cat_dir.glob("*.md")):
            if md_file.name == "README.md":
                continue
            edges = extract_from_file(md_file)
            all_edges.extend(edges)

    # Stats
    type_counts = {}
    for e in all_edges:
        type_counts[e["type"]] = type_counts.get(e["type"], 0) + 1

    print(f"[extract_edges] {len(all_edges)} edges extracted across {len(categories)} categories.",
          file=sys.stderr)
    for t, c in sorted(type_counts.items()):
        print(f"  {t}: {c}", file=sys.stderr)

    if args.format == "json":
        output = json.dumps(all_edges, indent=2)
    else:
        lines = [
            "# Edge Registry",
            "",
            f"Generated: {datetime.now(timezone.utc).isoformat()}",
            f"Total edges: {len(all_edges)}",
            "",
            "| # | Source | Target | Type | Evidence | Source File |",
            "|---|---|---|---|---|---|",
        ]
        for i, e in enumerate(all_edges, 1):
            ev = e["evidence"][:60].replace("|", "\\|") + ("..." if len(e["evidence"]) > 60 else "")
            lines.append(
                f"| {i} | `{e['source']}` | `{e['target']}` | `{e['type']}` | {ev} | `{e['source_file']}` |"
            )
        output = "\n".join(lines)

    if args.output == "-":
        print(output)
    else:
        Path(args.output).write_text(output, encoding="utf-8")
        print(f"[extract_edges] Written to {args.output}", file=sys.stderr)


if __name__ == "__main__":
    main()
