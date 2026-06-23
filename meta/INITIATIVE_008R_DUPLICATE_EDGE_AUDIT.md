# INITIATIVE-008R — Duplicate Edge Audit

**Date:** 2026-06-23  
**Phase:** 2  
**Status:** COMPLETE  
**Decision:** D-INIT-008R-001

## Definition

A duplicate edge is any pair of edges with identical `(source, target, type)` canonical key. Duplicate edges waste storage, inflate the reported edge count, and can cause double-weighting in graph traversal algorithms.

## Evidence Source

- File read: `.github/workflows/validate-graph.yml` (SHA: `667323ca`)
- Confirmed: No existing step validated edge uniqueness.
- The existing `Duplicate node ID check` step only checked node IDs, not edges.
- Classified as **Category A (already-pattern, disconnected)** in `meta/GOVERNANCE_GAP_CLASSIFICATION.md` — pattern identical to node dedup, applied to edge tuples.

## Pre-Implementation Graph State

| Metric | Value | Source |
|--------|-------|--------|
| Node count | 368 | `data/SKILLS_GRAPH.json` meta |
| Edge count | 774 | `data/SKILLS_GRAPH.json` meta |
| Schema version | 3.1 | `data/SKILLS_GRAPH.json` meta |
| Duplicate edges found (manual scan) | 0 | `(source, target, type)` key scan |

## Implementation

Added step `Duplicate edge check` to `.github/workflows/validate-graph.yml` immediately after the `Dangling target edge check` step.

**Logic:**
```python
seen = {}
dupes = []
for e in edges:
    key = (e["source"], e["target"], e.get("type", ""))
    if key in seen:
        dupes.append(e)
    else:
        seen[key] = True
if dupes:
    sys.exit(1)
```

**Canonical key:** `(source, target, type)` — a tuple of three strings.

Note: Two edges between the same source and target nodes with *different* types (e.g., `REQUIRES` vs `RECOMMENDED_WITH`) are **not** duplicates and will pass this check.

## Validation Result

| Check | Result | Count |
|-------|--------|-------|
| Duplicate edges in current graph | **PASS** | 0 duplicates found |
| CI step added | **ACTIVE** | Will block future PRs with duplicate edges |

## Impact

- **Before:** `build_graph.py` could theoretically emit the same `(source, target, type)` edge multiple times if a skill's prerequisite appeared in both `prerequisites` and `related_skills` with the same edge type, or if frontmatter was duplicated. This would inflate `edge_count` in `meta` without detection.
- **After:** Any duplicate `(source, target, type)` triple in `edges[]` will fail CI immediately at PR time.

## Status

`DUPLICATE_EDGE_DETECTION = ACTIVE`
