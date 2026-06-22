#!/usr/bin/env python3
"""
tools/build_graph.py — INITIATIVE-001 Phase C

Automated graph builder for skills-tree.

Pipeline:
  1. Discover all skills/*/  directories
  2. Parse YAML frontmatter from every skill .md file
  3. Invoke extract_edges.py logic to collect edges
  4. Collect REQUIRES edges from frontmatter `prerequisites` field (schema v3.1)
  5. Validate: no duplicate IDs, no self-loops, no orphan edges
  6. Write data/SKILLS_GRAPH.json
  7. Write data/SKILLS_GRAPH_STATS.json
  8. Write meta/GRAPH_BUILD_REPORT.md

Usage:
  python tools/build_graph.py
  python tools/build_graph.py --dry-run       # validate only, no writes
  python tools/build_graph.py --output path   # custom output path

NOTE: data/SKILLS_GRAPH.json is a GENERATED artifact.
      Never edit it manually — re-run this script instead.

SCHEMA v3.1 NOTE:
  Skills may declare a `prerequisites` YAML list in frontmatter.
  Each entry must be a canonical skill ID (category/slug format).
  These generate REQUIRES edges with source_method="frontmatter_prerequisite".
  No inference — only explicit author declarations are processed.
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
SCHEMA_VERSION = "3.1"   # bumped from 3.0 — INITIATIVE-004
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

    Supports:
      - Simple key: value pairs
      - Array values via YAML block sequences:
          prerequisites:
            - 02-reasoning/chain-of-thought
            - 02-reasoning/planning
    """
    text = md_path.read_text(encoding="utf-8")
    if not text.startswith("---"):
        return {}
    end = text.find("---", 3)
    if end == -1:
        return {}
    fm_block = text[3:end].strip()
    result = {}
    current_key = None
    current_list = None

    for line in fm_block.splitlines():
        # YAML list item under a key
        if line.startswith("  - ") or line.startswith("- "):
            item = line.lstrip().lstrip("- ").strip().strip('"')
            if current_key and current_list is not None:
                current_list.append(item)
            continue
        # Key: value line
        if ":" in line and not line.startswith(" "):
            current_list = None
            key, _, val = line.partition(":")
            key = key.strip()
            val = val.strip().strip('"')
            if val == "":
                # Start of a block sequence
                current_key = key
                current_list = []
                result[key] = current_list
            else:
                current_key = key
                result[key] = val
        # indented continuation (not a list item) — ignore

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

    # Read prerequisites from frontmatter (schema v3.1)
    # Only accepts list values — scalar values are silently ignored.
    raw_prereqs = fm.get("prerequisites", [])
    prerequisites = raw_prereqs if isinstance(raw_prereqs, list) else []

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
        "prerequisites": prerequisites,          # v3.1: explicit author declarations
        "related_skills": [],
        "source_file": str(md_path.relative_to(REPO_ROOT)),
        "quality_score": None,
    }


# ---------------------------------------------------------------------------
# REQUIRES edge builder (frontmatter_prerequisite source)
# ---------------------------------------------------------------------------
def build_prerequisite_edges(node: dict) -> list[dict]:
    """Generate REQUIRES edges from the node's prerequisites list.

    Source method: frontmatter_prerequisite
    Confidence: high (explicit author declaration)
    No inference — only processes what the author explicitly wrote.
    """
    edges = []
    source_id = node["id"]
    source_file = node["source_file"]

    for prereq_id in node.get("prerequisites", []):
        # Skip self-loops
        if prereq_id == source_id:
            continue
        edges.append({
            "source": source_id,
            "target": prereq_id,
            "type": "REQUIRES",
            "evidence": f"prerequisites: {prereq_id}",
            "source_file": source_file,
            "confidence": "high",
            "source_method": "frontmatter_prerequisite",
        })
    return edges


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
    """Extract RELATED_TO / SUPPORTS edges from a single markdown file.

    Note: REQUIRES edges from frontmatter prerequisites are handled by
    build_prerequisite_edges() — do not duplicate them here.
    """
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

        # Determine edge type from inline language
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
def validate_graph(nodes: list, edges: list) -> tuple[list, list]:
    """Run validation checks. Returns (errors, warnings)."""
    errors = []
    warnings = []
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
    for e in edges:
        if e["target"] not in node_ids:
            warnings.append(f"UNRESOLVED_TARGET: {e['target']} referenced from {e['source_file']}")

    return errors, warnings


# ---------------------------------------------------------------------------
# Build report
# ---------------------------------------------------------------------------
def write_build_report(nodes, edges, errors, warnings, output_path, dry_run):
    ts = datetime.now(timezone.utc).isoformat()
    requires_count = sum(1 for e in edges if e["type"] == "REQUIRES")
    supports_count = sum(1 for e in edges if e["type"] == "SUPPORTS")
    related_count = sum(1 for e in edges if e["type"] == "RELATED_TO")
    frontmatter_requires = sum(
        1 for e in edges
        if e["type"] == "REQUIRES" and e.get("source_method") == "frontmatter_prerequisite"
    )

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
        "| Metric | Value |",
        "|---|---|",
        f"| Total nodes | {len(nodes)} |",
        f"| Total edges | {len(edges)} |",
        f"| REQUIRES edges | {requires_count} |",
        f"| REQUIRES (frontmatter) | {frontmatter_requires} |",
        f"| SUPPORTS edges | {supports_count} |",
        f"| RELATED_TO edges | {related_count} |",
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
        for w in warnings[:50]:
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

            # Source 1: Related Skills section edges (RELATED_TO / SUPPORTS / inline REQUIRES)
            file_edges = extract_edges_from_file(md_file, source_id, known_ids)
            edges.extend(file_edges)

    # Source 2: frontmatter prerequisites → REQUIRES edges
    prereq_count = 0
    for node in nodes:
        prereq_edges = build_prerequisite_edges(node)
        edges.extend(prereq_edges)
        prereq_count += len(prereq_edges)

    if prereq_count > 0:
        print(f"  [prerequisites] {prereq_count} REQUIRES edges from frontmatter")

    print(f"  [edges] {len(edges)} total edges")

    errors, warnings = validate_graph(nodes, edges)
    write_build_report(nodes, edges, errors, warnings, args.output, args.dry_run)

    if errors:
        print(f"  [FAIL] {len(errors)} validation errors. Graph not written.")
        for e in errors:
            print(f"    ERROR: {e}")
        sys.exit(1)

    requires_count = sum(1 for e in edges if e["type"] == "REQUIRES")
    graph = {
        "meta": {
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "generator": GENERATOR,
            "schema_version": SCHEMA_VERSION,
            "node_count": len(nodes),
            "edge_count": len(edges),
            "requires_count": requires_count,
            "initiative": "INITIATIVE-004",
        },
        "nodes": nodes,
        "edges": edges,
    }

    stats = {
        "generated_at": graph["meta"]["generated_at"],
        "node_count": len(nodes),
        "edge_count": len(edges),
        "requires_count": requires_count,
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

    print(f"[build_graph] DONE — {len(nodes)} nodes, {len(edges)} edges "
          f"({requires_count} REQUIRES), {len(warnings)} warnings.")


if __name__ == "__main__":
    main()
