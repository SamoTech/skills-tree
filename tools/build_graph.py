#!/usr/bin/env python3
"""
tools/build_graph.py — INITIATIVE-001 Phase C

Automated graph builder for skills-tree.

Pipeline:
  1. Discover all skills/*/  directories
  2. Parse YAML frontmatter from every skill .md file
  3. Invoke extract_edges.py logic to collect edges
  4. Validate: no duplicate IDs, no self-loops, no orphan edges
  5. Write data/SKILLS_GRAPH.json
  6. Write data/SKILLS_GRAPH_STATS.json
  7. Write meta/GRAPH_BUILD_REPORT.md

Usage:
  python tools/build_graph.py
  python tools/build_graph.py --dry-run       # validate only, no writes
  python tools/build_graph.py --output path   # custom output path

NOTE: data/SKILLS_GRAPH.json is a GENERATED artifact.
      Never edit it manually — re-run this script instead.
"""

import argparse
import json
import os
import sys
import re
from datetime import datetime, timezone
from pathlib import Path

# ---------------------------------------------------------------------------
# Paths (relative to repo root)
# ---------------------------------------------------------------------------
REPO_ROOT = Path(__file__).parent.parent
SKILLS_DIR = REPO_ROOT / "skills"
DATA_DIR = REPO_ROOT / "data"
META_DIR = REPO_ROOT / "meta"
SCHEMA_VERSION = "3.0"
GENERATOR = "tools/build_graph.py"

# ---------------------------------------------------------------------------
# Layer mapping (Phase F — category → layer)
# ---------------------------------------------------------------------------
LAYER_MAP = {
    "01-perception": "perception",
    "02-reasoning": "reasoning",
    "03-memory": "reasoning",
    "04-context": "reasoning",
    "05-output": "execution",
    "06-code": "execution",
    "07-tool-use": "execution",
    "08-evaluation": "systems",
    "09-agentic-patterns": "systems",
    "10-safety": "systems",
    "11-multimodal": "perception",
    "12-data": "execution",
    "13-deployment": "systems",
}


# ---------------------------------------------------------------------------
# Frontmatter parser
# ---------------------------------------------------------------------------
def parse_frontmatter(md_path: Path) -> dict:
    """Extract YAML frontmatter from a markdown file.
    Returns empty dict if no frontmatter found.
    """
    text = md_path.read_text(encoding="utf-8")
    if not text.startswith("---"):
        return {}
    end = text.find("---", 3)
    if end == -1:
        return {}
    fm_block = text[3:end].strip()
    result = {}
    for line in fm_block.splitlines():
        if ":" in line:
            key, _, val = line.partition(":")
            result[key.strip()] = val.strip().strip('"')
    return result


# ---------------------------------------------------------------------------
# Skill node builder
# ---------------------------------------------------------------------------
def build_node(md_path: Path, category: str) -> dict | None:
    """Build a canonical skill node from a markdown file."""
    fm = parse_frontmatter(md_path)
    if not fm:
        return None  # skip files with no frontmatter

    skill_slug = md_path.stem
    skill_id = f"{category}/{skill_slug}"

    return {
        "id": skill_id,
        "title": fm.get("title", skill_slug.replace("-", " ").title()),
        "category": category,
        "layer": LAYER_MAP.get(category, "systems"),
        "level": fm.get("level", "basic"),
        "stability": fm.get("stability", "stable"),
        "version": fm.get("version", "v1"),
        "added": fm.get("added", None),
        "tags": [],
        "related_skills": [],
        "source_file": str(md_path.relative_to(REPO_ROOT)),
        "quality_score": None,
    }


# ---------------------------------------------------------------------------
# Edge extraction (inline — see also tools/extract_edges.py for full engine)
# ---------------------------------------------------------------------------
REQUIRES_TRIGGERS = [
    r"prerequisite", r"depends on", r"requires", r"before learning", r"foundation skill"
]
SUPPORTS_TRIGGERS = [
    r"supports", r"enables", r"extends", r"powers", r"executes", r"builds on"
]
RELATED_SECTION_RE = re.compile(
    r"##\s+Related Skills?\s*\n(.*?)(?=\n##|\Z)", re.DOTALL | re.IGNORECASE
)
MD_LINK_RE = re.compile(r"\[([^\]]+)\]\(([^)]+\.md)\)")


def extract_edges_from_file(md_path: Path, source_id: str, known_ids: set) -> list:
    """Extract edges from a single markdown file."""
    edges = []
    text = md_path.read_text(encoding="utf-8")
    category = md_path.parent.name

    # Find Related Skills section
    match = RELATED_SECTION_RE.search(text)
    if not match:
        return edges

    section = match.group(1)
    for link_match in MD_LINK_RE.finditer(section):
        link_text = link_match.group(1)
        link_href = link_match.group(2)
        evidence = link_match.group(0)

        # Resolve target ID
        if link_href.startswith("../"):
            # cross-category link
            parts = link_href.lstrip("../").split("/")
            if len(parts) == 2:
                target_cat = parts[0]
                target_slug = parts[1].replace(".md", "")
                target_id = f"{target_cat}/{target_slug}"
            else:
                continue
        else:
            target_slug = link_href.replace(".md", "").split("/")[-1]
            target_id = f"{category}/{target_slug}"

        # Determine edge type
        edge_type = "RELATED_TO"
        lower_evidence = evidence.lower() + " " + link_text.lower()
        if any(re.search(p, lower_evidence) for p in REQUIRES_TRIGGERS):
            edge_type = "REQUIRES"
        elif any(re.search(p, lower_evidence) for p in SUPPORTS_TRIGGERS):
            edge_type = "SUPPORTS"

        # Skip self-loops
        if source_id == target_id:
            continue

        edges.append({
            "source": source_id,
            "target": target_id,
            "type": edge_type,
            "evidence": evidence.strip(),
            "source_file": str(md_path.relative_to(REPO_ROOT)),
            "confidence": "high",
        })

    return edges


# ---------------------------------------------------------------------------
# Validation
# ---------------------------------------------------------------------------
def validate_graph(nodes: list, edges: list) -> list:
    """Run validation checks. Returns list of error strings (empty = pass)."""
    errors = []
    node_ids = {n["id"] for n in nodes}

    # Duplicate node IDs
    seen_ids = set()
    for n in nodes:
        if n["id"] in seen_ids:
            errors.append(f"DUPLICATE_NODE: {n['id']}")
        seen_ids.add(n["id"])

    # Duplicate edges
    seen_edges = set()
    for e in edges:
        key = (e["source"], e["target"], e["type"])
        if key in seen_edges:
            errors.append(f"DUPLICATE_EDGE: {e['source']} --{e['type']}--> {e['target']}")
        seen_edges.add(key)

    # Self-loops
    for e in edges:
        if e["source"] == e["target"]:
            errors.append(f"SELF_LOOP: {e['source']}")

    # Orphan source references
    for e in edges:
        if e["source"] not in node_ids:
            errors.append(f"INVALID_SOURCE: {e['source']} in {e['source_file']}")

    # Unresolved target references (warnings, not errors)
    unresolved = []
    for e in edges:
        if e["target"] not in node_ids:
            unresolved.append(f"UNRESOLVED_TARGET: {e['target']} referenced from {e['source_file']}")

    return errors, unresolved


# ---------------------------------------------------------------------------
# Build report
# ---------------------------------------------------------------------------
def write_build_report(nodes, edges, errors, warnings, output_path, dry_run):
    ts = datetime.now(timezone.utc).isoformat()
    lines = [
        "# Graph Build Report",
        "",
        f"**Generated:** {ts}  ",
        f"**Generator:** {GENERATOR}  ",
        f"**Schema Version:** {SCHEMA_VERSION}  ",
        f"**Dry Run:** {dry_run}  ",
        "",
        "## Metrics",
        "",
        f"| Metric | Value |",
        f"|---|---|",
        f"| Total nodes | {len(nodes)} |",
        f"| Total edges | {len(edges)} |",
        f"| Validation errors | {len(errors)} |",
        f"| Unresolved targets (warnings) | {len(warnings)} |",
        "",
    ]
    if errors:
        lines += ["## Validation Errors (FAIL)", ""]
        for e in errors:
            lines.append(f"- `{e}`")
        lines.append("")
    if warnings:
        lines += ["## Unresolved Target Warnings", ""]
        for w in warnings[:50]:  # cap at 50 for readability
            lines.append(f"- `{w}`")
        lines.append("")
    if not errors:
        lines += ["## Status", "", "✅ **PASS** — graph generated successfully.", ""]
    else:
        lines += ["## Status", "", "❌ **FAIL** — validation errors must be resolved.", ""]

    report_path = META_DIR / "GRAPH_BUILD_REPORT.md"
    if not dry_run:
        report_path.write_text("\n".join(lines), encoding="utf-8")
        print(f"  [report] {report_path}")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(description="Build SKILLS_GRAPH.json from source files.")
    parser.add_argument("--dry-run", action="store_true", help="Validate only, no file writes.")
    parser.add_argument("--output", default=str(DATA_DIR / "SKILLS_GRAPH.json"),
                        help="Output path for SKILLS_GRAPH.json.")
    args = parser.parse_args()

    print("[build_graph] Scanning skill files...")
    nodes = []
    edges = []

    for cat_dir in sorted(SKILLS_DIR.iterdir()):
        if not cat_dir.is_dir():
            continue
        category = cat_dir.name
        if not re.match(r"^[0-9]{2}-", category):
            continue

        for md_file in sorted(cat_dir.glob("*.md")):
            if md_file.name == "README.md":
                continue
            node = build_node(md_file, category)
            if node:
                nodes.append(node)

    print(f"  [nodes] {len(nodes)} nodes discovered")
    known_ids = {n["id"] for n in nodes}

    for cat_dir in sorted(SKILLS_DIR.iterdir()):
        if not cat_dir.is_dir():
            continue
        category = cat_dir.name
        if not re.match(r"^[0-9]{2}-", category):
            continue
        for md_file in sorted(cat_dir.glob("*.md")):
            if md_file.name == "README.md":
                continue
            source_id = f"{category}/{md_file.stem}"
            file_edges = extract_edges_from_file(md_file, source_id, known_ids)
            edges.extend(file_edges)

    print(f"  [edges] {len(edges)} edges extracted")

    errors, warnings = validate_graph(nodes, edges)
    write_build_report(nodes, edges, errors, warnings, args.output, args.dry_run)

    if errors:
        print(f"  [FAIL] {len(errors)} validation errors. Graph not written.")
        for e in errors:
            print(f"    ERROR: {e}")
        sys.exit(1)

    graph = {
        "meta": {
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "generator": GENERATOR,
            "schema_version": SCHEMA_VERSION,
            "node_count": len(nodes),
            "edge_count": len(edges),
            "initiative": "INITIATIVE-001 V3",
        },
        "nodes": nodes,
        "edges": edges,
    }

    stats = {
        "generated_at": graph["meta"]["generated_at"],
        "node_count": len(nodes),
        "edge_count": len(edges),
        "nodes_by_level": {},
        "nodes_by_layer": {},
        "nodes_by_category": {},
        "edges_by_type": {},
    }
    for n in nodes:
        stats["nodes_by_level"][n["level"]] = stats["nodes_by_level"].get(n["level"], 0) + 1
        stats["nodes_by_layer"][n["layer"]] = stats["nodes_by_layer"].get(n["layer"], 0) + 1
        stats["nodes_by_category"][n["category"]] = stats["nodes_by_category"].get(n["category"], 0) + 1
    for e in edges:
        stats["edges_by_type"][e["type"]] = stats["edges_by_type"].get(e["type"], 0) + 1

    if not args.dry_run:
        DATA_DIR.mkdir(parents=True, exist_ok=True)
        output_path = Path(args.output)
        output_path.write_text(json.dumps(graph, indent=2), encoding="utf-8")
        print(f"  [write] {output_path}")
        stats_path = DATA_DIR / "SKILLS_GRAPH_STATS.json"
        stats_path.write_text(json.dumps(stats, indent=2), encoding="utf-8")
        print(f"  [write] {stats_path}")

    print(f"[build_graph] DONE — {len(nodes)} nodes, {len(edges)} edges, {len(warnings)} warnings.")


if __name__ == "__main__":
    main()
