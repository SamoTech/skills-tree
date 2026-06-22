# INITIATIVE-002B Final Report
## Dependency Model Strategy Audit

**Date:** 2026-06-22  
**Status:** COMPLETE  
**Commit:** (this commit)

---

## Pre-Flight Verification

| Check | Result |
|---|---|
| REQUIRES_EDGES = 0 | ✅ CONFIRMED (source: INITIATIVE_001C_AUDIT_REPORT.md) |
| CANDIDATE_COUNT = 5 | ✅ CONFIRMED (source: INITIATIVE_002A_FINAL_REPORT.md) |
| GRAPH_UPGRADE_FEASIBLE = YES | ✅ CONFIRMED (source: INITIATIVE_002A_FINAL_REPORT.md) |

No STATE_DIVERGENCE_REPORT required.

---

## Phase Summary

### Phase 1 — Content Coverage Audit
File: `meta/DEPENDENCY_COVERAGE_AUDIT.md`

Key finding: **1.4% dependency language coverage** (5 LEVEL 3 occurrences across 367 nodes). The `related_skills` schema field exists but carries no semantic type. No `prerequisites` field exists in the schema.

### Phase 2 — Authoring Model Audit
File: `meta/INITIATIVE_002B_AUTHORING_MODEL_AUDIT.md`

Key finding: **The schema does NOT support prerequisite authoring.** `additionalProperties: false` in `skill.schema.json` would reject any `prerequisites` field added to frontmatter today. `extract_edges.py` docstring references a `dependencies` frontmatter field that was never added to the schema — a confirmed code/schema divergence.

### Phase 3 — Recommendation Engine Requirements
File: `meta/RECOMMENDATION_DEPENDENCY_ANALYSIS.md`

Key finding: **`recommend.py` is architecturally complete but functionally blocked.** Stage 2 (backward BFS) filters exclusively on `edge_type == "REQUIRES"`. With 0 REQUIRES edges, the engine returns keyword-matched skills in arbitrary alphabetical order — not a learning path. No fallback behavior exists.

Minimum viable REQUIRES edges: ~50 for 1-hop paths, ~150–200 for useful 2–3 hop paths.

### Phase 4 — Strategic Options
File: `meta/INITIATIVE_002B_STRATEGIC_OPTIONS.md`

| Option | Verdict |
|---|---|
| A — Extraction only | Not sufficient (1.4% coverage) |
| B — Schema authoring only | Correct long-term target; high upfront cost |
| C — Hybrid | **Recommended** |

---

## Phase 5 — Decision

| Field | Value |
|---|---|
| **CURRENT_MODEL** | Extraction-only (Option A), de facto — 0 REQUIRES edges generated |
| **TARGET_MODEL** | Hybrid (Option C): immediate extraction of 5 confirmed candidates → schema field addition → incremental backfill |
| **RATIONALE** | The extraction engine is built and ready. The schema gap (`prerequisites` field missing) is the single highest-leverage fix. Adding the field unblocks: (1) author-declared prerequisites on new skills, (2) extraction from frontmatter (already supported by `extract_edges.py` Source 2), (3) CI validation. The 5 extracted candidates provide immediate pilot data for `recommend.py` without waiting for full backfill. |

---

## Implementation Prerequisites for INITIATIVE-003

Before INITIATIVE-003 can add REQUIRES edges at scale, the following must be true:

1. `schema/skill.schema.json` must add `prerequisites` as an optional array field
2. `extract_edges.py` Source 2 (frontmatter `dependencies` field) must be aligned with the new schema field name
3. A contribution guide must document how to declare prerequisites
4. The 5 LEVEL 3 candidates from INITIATIVE-002A must be written to the graph (pilot step)

---

## Final Decision

| | |
|---|---|
| **DEPENDENCY_DATA_PRESENT** | **NO** — 0 REQUIRES edges in graph; 5 candidates in audit file only |
| **EXPLICIT_PREREQUISITES_FOUND** | **0 LEVEL 1/2** · **5 LEVEL 3** · 3 LEVEL 4 (rejected) |
| **RECOMMENDATION_ENGINE_VIABLE** | **NO** — BFS stage blocked; returns arbitrary ordering |
| **RECOMMENDED_MODEL** | **C (Hybrid)** |
| **NEXT_INITIATIVE** | **INITIATIVE-003** |
