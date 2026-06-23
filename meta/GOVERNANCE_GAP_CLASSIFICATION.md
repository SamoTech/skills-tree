# GOVERNANCE_GAP_CLASSIFICATION.md

**Initiative:** INITIATIVE-007R — Governance Reality Check  
**Date:** 2026-06-23  
**Evidence basis:** Direct reads of repository files only.

---

## Classification Schema

- **Category A** — Already implemented but disconnected (code exists, not wired to CI or not consuming output)
- **Category B** — Partially implemented (logic exists but incomplete, degraded, or coverage gaps)
- **Category C** — Completely missing (no code, no workflow step, no output)

---

## Gap 1 — Dangling Target Detection

**Classification: Category A — Implemented but disconnected (one side only)**

`validate-graph.yml` step `Invalid source edge check` (SHA `667323ca`) checks:
```python
invalid = [e for e in data.get("edges", []) if e["source"] not in node_ids]
```
This validates the *source* side. The identical logic for the *target* side:
```python
invalid = [e for e in data.get("edges", []) if e["target"] not in node_ids]
```
does not exist as a workflow step. The pattern is proven to work (source check passes CI). Adding target check requires adding one workflow step with ~10 lines of inline Python, identical structure to the existing step.

**Effort to close:** Minimal. Copy existing step, change `source` → `target`.

---

## Gap 2 — Duplicate Edge Detection

**Classification: Category A — Implemented but disconnected (node version exists, edge version missing)**

`validate-graph.yml` step `Duplicate node ID check` (SHA `667323ca`) implements:
```python
ids = [n["id"] for n in data.get("nodes", [])]
dupes = [i for i in ids if ids.count(i) > 1]
```
The identical structural pattern for edges:
```python
sig = [(e["source"], e["target"], e["type"]) for e in data.get("edges", [])]
dupes = [s for s in sig if sig.count(s) > 1]
```
does not exist. The problem is understood and the solution pattern is proven.

**Effort to close:** Minimal. Add one workflow step, ~12 lines inline Python.

---

## Gap 3 — Cycle Detection

**Classification: Category B — Partially implemented, not wired to CI**

`recommend.py` `topological_sort()` (SHA `3d95d515` lines 111–129) contains cycle detection logic at lines 126–129:
```python
if not ready:  # cycle detected — add arbitrarily
    ready = [sorted(remaining)[0]]
```
The detection logic fires (the `if not ready` branch is reached when a cycle exists) but the response is suppression, not reporting. The function signature returns `list[str]`, not a result that can signal a cycle. No CI workflow calls this function. The fix requires: (1) add a return signal or raise, (2) add a CI step that calls `recommend.py` in validation mode (or a dedicated cycle checker).

**Effort to close:** Medium. Requires modifying `recommend.py` or writing a new graph cycle checker script, then wiring to `validate-graph.yml`.

---

## Gap 4 — Invalid Edge Type Detection

**Classification: Category C — Completely missing**

No code in any of the four read files validates that `edge.type` belongs to a permitted set. `schema/edge.schema.json` presumably defines valid types but is not read by any runtime workflow step. There is no inline Python in `validate-graph.yml` that loads the edge schema and cross-validates edge types.

**Effort to close:** Medium. Requires: (1) reading permitted types from `schema/edge.schema.json` at runtime, (2) comparing all edge type values, (3) failing on unknowns.

---

## Gap 5 — Unreachable Node / Orphan Detection

**Classification: Category C — Completely missing**

No graph traversal computing in-degree or out-degree exists in any of the four files. No BFS/DFS from root nodes exists in any workflow step. `recommend.py` performs backward BFS but only from a matched seed set, not from all nodes, and only at query time (not CI time).

**Effort to close:** Medium. Requires a new script or inline workflow step that computes in-degree for all nodes and reports those with in-degree = 0 and no designated root status.

---

## Gap 6 — Learning Path Validation

**Classification: Category B — Partially implemented, not a CI gate**

`recommend.py` traverses REQUIRES edges via backward BFS (`resolve_dependencies()`, lines 74–87) and performs topological sort (`topological_sort()`, lines 90–129). This constitutes partial learning path logic. However:
1. It is a query-time tool, not a CI validation step.
2. It does not validate that every REQUIRES edge has a reachable prerequisite from a global perspective.
3. It does not compute or report path depth metrics.
4. It is never invoked by any workflow.

**Effort to close:** Medium-High. Requires a standalone validator that iterates all REQUIRES edges, checks reachability, computes depth, and exits non-zero on failures — then CI integration.

---

## Gap 7 — Recommendation Quality Validation

**Classification: Category B — Logic present, data absent**

`recommend.py` `match_goal_to_skills()` includes tag matching logic that would improve recommendation quality. However, all 368 nodes have `tags: []` (MEMORY_STATE.md SHA `1d7e0d5f`). The code path executes but contributes nothing. Additionally, there is no quality threshold — the function returns whatever score > 0 matches, even if only one keyword matches in the ID string.

**Effort to close:** Two separate efforts: (1) populate tags — HIGH effort (368 nodes), (2) add score threshold — LOW effort (one `if score >= threshold` line).

---

## Gap 8 — Quality Threshold Enforcement as PR Gate

**Classification: Category A — Computed but not gated**

`validate-graph.yml` `quality-report` job runs `tools/quality_score.py` and commits `meta/SKILL_QUALITY_INDEX.md` on push to main. The score is computed and persisted. However, no PR workflow reads this score and blocks merge if the score decreases. The gate mechanism requires only: reading the previous score from the committed file and comparing to the PR-time score.

**Effort to close:** Medium. Requires adding a PR-triggered step that reads the stored quality index, computes the current score, and fails if delta is negative beyond a threshold.

---

## Classification Summary

| Gap | Classification | Effort |
|---|---|---|
| Dangling Target Detection | **Category A** | Minimal |
| Duplicate Edge Detection | **Category A** | Minimal |
| Quality Threshold Enforcement | **Category A** | Medium |
| Cycle Detection | **Category B** | Medium |
| Learning Path Validation | **Category B** | Medium-High |
| Recommendation Quality Validation | **Category B** | Mixed (tags=High, threshold=Low) |
| Invalid Edge Type Detection | **Category C** | Medium |
| Unreachable Node / Orphan Detection | **Category C** | Medium |

### Category Distribution

- **Category A (disconnect only):** 3 gaps — highest ROI, existing logic, just needs wiring
- **Category B (partial):** 3 gaps — logic exists but incomplete or ungated
- **Category C (missing):** 2 gaps — require net-new implementation

---

*No synthetic metrics. No inferred relationships. All findings traceable to direct file reads.*
