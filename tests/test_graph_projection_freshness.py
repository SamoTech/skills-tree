"""Freshness contract for the committed skills-graph projections.

`data/SKILLS_GRAPH.json` and `docs/api/graph.json` are generated projections of
the canonical `skills/` corpus, republished through the generated-graph
automation PR. The "Build Graph & Validate" workflow validates the freshly
generated graph's schema and integrity on every PR, but it never requires
equality with the committed artifacts — a corpus change that outlives its
graph automation PR keeps CI green while publishing a stale projection.

This test closes that gap by re-deriving the graph in-memory from the
canonical corpus on every push (reusing `tools.build_graph`'s own node and
edge builders; no files written, xdist-safe) and requiring equality with the
committed projections. Only the wall-clock `meta.generated_at` field is
excluded from the comparison (it is not derivable and is already normalized
away by the automation's semantic-diff step).
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from tools import build_graph
from tools.skill_corpus import is_public_category

SKILLS_DIR = ROOT / "skills"
DATA_GRAPH = ROOT / "data" / "SKILLS_GRAPH.json"
API_GRAPH = ROOT / "docs" / "api" / "graph.json"

# Only `meta.generated_at` is wall-clock; every other field is derived from
# repository state and must match byte-for-byte after parsing.
META_EXCLUDED = {"generated_at"}


def _fresh_projection() -> tuple[list, list]:
    """Replicate build_graph.main()'s scan loop without writing any files."""
    nodes: list = []
    for cat_dir in sorted(SKILLS_DIR.iterdir()):
        if not cat_dir.is_dir():
            continue
        category = cat_dir.name
        if not re.match(r"^[0-9]{2}-", category) or not is_public_category(category):
            continue
        for md_file in sorted(cat_dir.glob("*.md")):
            if md_file.name == "README.md":
                continue
            node = build_graph.build_node(md_file, category)
            if node:
                nodes.append(node)

    known_ids = {n["id"] for n in nodes}
    edges: list = []
    for cat_dir in sorted(SKILLS_DIR.iterdir()):
        if not cat_dir.is_dir():
            continue
        category = cat_dir.name
        if not re.match(r"^[0-9]{2}-", category) or not is_public_category(category):
            continue
        for md_file in sorted(cat_dir.glob("*.md")):
            if md_file.name == "README.md":
                continue
            source_id = f"{category}/{md_file.stem}"
            edges.extend(build_graph.extract_edges_from_file(md_file, source_id, known_ids))

    for node in nodes:
        edges.extend(build_graph.build_prerequisite_edges(node))

    errors, warnings = build_graph.validate_graph(nodes, edges)
    assert not errors, "freshly derived graph has validation errors: " + "; ".join(errors[:10])
    return nodes, edges


def _describe_drift(committed_nodes: list, fresh_nodes: list,
                    committed_edges: list, fresh_edges: list) -> str:
    committed_ids = {n["id"] for n in committed_nodes}
    fresh_ids = {n["id"] for n in fresh_nodes}
    node_drift = sorted(committed_ids ^ fresh_ids)

    def edge_key(edge: dict) -> tuple:
        return (edge["source"], edge["target"], edge["type"], edge.get("evidence"))

    committed_edge_keys = {edge_key(e) for e in committed_edges}
    fresh_edge_keys = {edge_key(e) for e in fresh_edges}
    edge_drift = sorted(committed_edge_keys ^ fresh_edge_keys)
    return (
        f"node drift (first 10): {node_drift[:10]} "
        f"edge drift (first 10): {edge_drift[:10]}"
    )


def test_committed_data_graph_is_fresh_projection_of_canonical_corpus() -> None:
    fresh_nodes, fresh_edges = _fresh_projection()
    committed = json.loads(DATA_GRAPH.read_text(encoding="utf-8"))

    assert committed["nodes"] == fresh_nodes, (
        "data/SKILLS_GRAPH.json nodes are stale relative to skills/; merge the "
        "pending generated-graph automation PR (or re-run tools/build_graph.py). "
        + _describe_drift(committed["nodes"], fresh_nodes,
                          committed["edges"], fresh_edges)
    )
    assert committed["edges"] == fresh_edges, (
        "data/SKILLS_GRAPH.json edges are stale relative to skills/; merge the "
        "pending generated-graph automation PR (or re-run tools/build_graph.py). "
        + _describe_drift(committed["nodes"], fresh_nodes,
                          committed["edges"], fresh_edges)
    )


def test_committed_graph_meta_counts_match_fresh_derivation() -> None:
    fresh_nodes, fresh_edges = _fresh_projection()
    committed = json.loads(DATA_GRAPH.read_text(encoding="utf-8"))
    meta = committed["meta"]

    requires_count = sum(1 for e in fresh_edges if e["type"] == "REQUIRES")
    expected_meta = {
        "generator": build_graph.GENERATOR,
        "schema_version": build_graph.SCHEMA_VERSION,
        "node_count": len(fresh_nodes),
        "edge_count": len(fresh_edges),
        "requires_count": requires_count,
    }
    for key, value in expected_meta.items():
        assert meta.get(key) == value, (
            f"data/SKILLS_GRAPH.json meta.{key} is {meta.get(key)!r} but the "
            f"canonical corpus derives {value!r}; the committed graph "
            "projection is stale"
        )
    assert set(meta) - META_EXCLUDED, "committed graph lost its meta block"


def test_docs_api_graph_matches_data_projection() -> None:
    assert API_GRAPH.read_bytes() == DATA_GRAPH.read_bytes(), (
        "docs/api/graph.json is not byte-identical to data/SKILLS_GRAPH.json; "
        "the graph automation publishes both from the same build and they "
        "must not diverge"
    )
