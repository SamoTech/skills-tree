# INITIATIVE-008R — Dangling Target Audit

**Date:** 2026-06-23  
**Phase:** 1  
**Status:** COMPLETE  
**Decision:** D-INIT-008R-001

## Definition

A dangling target is an edge where `edge.target` does not exist in the node registry. This is the symmetric counterpart to the existing invalid-source check. A dangling target means a skill declares a dependency on a node that does not exist in the graph, which corrupts learning path generation.

## Evidence Source

- File read: `.github/workflows/validate-graph.yml` (SHA: `667323ca`)
- Confirmed: The existing `Invalid source edge check` step validates `edge.source` but **no step validated `edge.target`**.
- This was classified as **Category A (already-pattern, disconnected)** in `meta/GOVERNANCE_GAP_CLASSIFICATION.md`.

## Pre-Implementation Graph State

| Metric | Value | Source |
|--------|-------|--------|
| Node count | 368 | `data/SKILLS_GRAPH.json` meta |
| Edge count | 774 | `data/SKILLS_GRAPH.json` meta |
| Schema version | 3.1 | `data/SKILLS_GRAPH.json` meta |
| Dangling targets found (manual scan) | 0 | All node `prerequisites` fields checked against node registry |

## Implementation

Added step `Dangling target edge check` to `.github/workflows/validate-graph.yml` immediately after the `Invalid source edge check` step.

**Logic:**
```python
node_ids = {n["id"] for n in data.get("nodes", [])}
dangling = [e for e in data.get("edges", []) if e["target"] not in node_ids]
if dangling:
    print(f"FAIL: {len(dangling)} edges with dangling (missing) target node IDs.")
    sys.exit(1)
```

**Canonical key validated:** `edge.target ∈ node_ids`

## Validation Result

| Check | Result | Count |
|-------|--------|-------|
| Dangling targets in current graph | **PASS** | 0 dangling targets found |
| CI step added | **ACTIVE** | Will block future PRs with dangling targets |

## Impact

- **Before:** A skill could reference a non-existent node as a prerequisite. The invalid-source check only caught edges with bad sources, not bad targets. A dangling target would be silently ignored by `resolve_dependencies()` in `recommend.py`, producing incomplete learning paths.
- **After:** Any edge whose `target` is not a registered node ID will fail CI immediately at PR time.

## Status

`DANGLING_TARGET_DETECTION = ACTIVE`
