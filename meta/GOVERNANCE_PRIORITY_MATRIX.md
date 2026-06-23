# GOVERNANCE_PRIORITY_MATRIX.md

**Initiative:** INITIATIVE-007R — Governance Reality Check  
**Date:** 2026-06-23  
**Evidence basis:** Direct reads of repository files only. Priority rankings derived from gap classification and evidence — no subjective scoring.

---

## Priority Framework

Work is ranked across four tiers, ordered by **leverage** (impact per implementation effort):

1. **Tier 1 — Existing Code Activation** (Category A gaps — already implemented, just disconnected)
2. **Tier 2 — Existing Workflow Integration** (Category B gaps — logic exists, needs CI wiring)
3. **Tier 3 — Missing Validator Implementation** (Category C gaps — net-new code required)
4. **Tier 4 — New Governance Features** (beyond current gap scope)

---

## Tier 1 — Existing Code Activation (Highest ROI)

These gaps require adding ~10–20 lines to an existing workflow file. No new tools. No new logic. Pattern already proven in CI.

### 1A — Add Dangling Target Detection step to `validate-graph.yml`

**Gap classification:** Category A (GOVERNANCE_GAP_CLASSIFICATION.md Gap 1)  
**Evidence:** `validate-graph.yml` already has `Invalid source edge check`. Identical step for target side is absent.  
**Implementation:** Copy step, change `e["source"]` → `e["target"]`. ~10 lines inline Python.  
**CI impact:** Blocks PRs that introduce edges pointing to non-existent node IDs.  
**Risk:** Near zero. Identical pattern already passing CI.  

### 1B — Add Duplicate Edge Detection step to `validate-graph.yml`

**Gap classification:** Category A (GOVERNANCE_GAP_CLASSIFICATION.md Gap 2)  
**Evidence:** `validate-graph.yml` already has `Duplicate node ID check`. Edge duplicate check uses same structure.  
**Implementation:** Add step with tuple signature `(source, target, type)` deduplication. ~12 lines inline Python.  
**CI impact:** Blocks PRs that introduce redundant edges.  
**Risk:** Near zero. Identical pattern already passing CI.  

### 1C — Wire Quality Score to PR Gate

**Gap classification:** Category A (GOVERNANCE_GAP_CLASSIFICATION.md Gap 8)  
**Evidence:** `quality-report` job in `validate-graph.yml` computes and commits `SKILL_QUALITY_INDEX.md` on main push. Score is available but no PR step reads it.  
**Implementation:** Add a PR-triggered step that reads stored score from `SKILL_QUALITY_INDEX.md`, runs `quality_score.py` in read mode, compares delta, exits 1 if below threshold.  
**CI impact:** Blocks PRs that regress graph quality score.  
**Risk:** Low-Medium. Requires defining threshold value. Risk: over-aggressive threshold blocks legitimate PRs.  
**Dependency:** `tools/quality_score.py` internals not read — must be confirmed to support comparison mode before implementation.  

---

## Tier 2 — Existing Workflow Integration (Medium ROI)

Logic partially exists but is not wired to CI or its output is never consumed as a gate.

### 2A — Fix Cycle Detection in `recommend.py` and Wire to CI

**Gap classification:** Category B (GOVERNANCE_GAP_CLASSIFICATION.md Gap 3)  
**Evidence:** `recommend.py` lines 126–129 detect cycles but suppress them silently. No CI step invokes this detection path.  
**Implementation (two parts):**
- Part 1: Modify `topological_sort()` to raise `ValueError` (or return a sentinel) when `not ready` and `remaining` is non-empty.
- Part 2: Add a CI step in `validate-graph.yml` that runs a graph traversal script and fails on cycle detection.
**CI impact:** Blocks PRs that introduce REQUIRES cycles into the graph.  
**Risk:** Medium. Modifying `recommend.py` may affect recommendation output behavior. Requires regression check.  

### 2B — Wire Learning Path Validation to CI

**Gap classification:** Category B (GOVERNANCE_GAP_CLASSIFICATION.md Gap 6)  
**Evidence:** `recommend.py` traverses REQUIRES edges via `resolve_dependencies()` and `topological_sort()` but only at query time. No CI step invokes path validation.  
**Implementation:** Extract or duplicate the backward BFS logic into a standalone `validate_learning_paths.py` script. CI step calls it and fails on unreachable prerequisites or cycle-broken paths.  
**CI impact:** Blocks PRs where a REQUIRES edge references a prerequisite that cannot be reached.  
**Risk:** Medium. New standalone script needed. Depends on cycle detection fix (2A) first.  

### 2C — Add Score Threshold to Recommendation Quality

**Gap classification:** Category B partial — low-effort portion (GOVERNANCE_GAP_CLASSIFICATION.md Gap 7)  
**Evidence:** `recommend.py` `match_goal_to_skills()` returns all `score > 0` matches with no floor.  
**Implementation:** Add a minimum score threshold parameter (e.g., `--min-score 2`) that filters out single-keyword matches.  
**CI impact:** None directly — `recommend.py` is not a CI step. Improves runtime recommendation quality.  
**Risk:** Low. One conditional filter line.  

---

## Tier 3 — Missing Validator Implementation (Net-New)

No existing logic to build on. Requires new tools.

### 3A — Invalid Edge Type Detection

**Gap classification:** Category C (GOVERNANCE_GAP_CLASSIFICATION.md Gap 4)  
**Evidence:** No code validates `edge.type` against permitted values. `schema/edge.schema.json` exists but is not consumed at runtime.  
**Implementation:** New inline CI step or `validate_edge_types.py` script. Reads permitted types from `schema/edge.schema.json`. Checks all graph edges. Exits 1 on unknown types.  
**CI impact:** Blocks PRs introducing edges with invalid or misspelled type values.  
**Risk:** Low-Medium. Requires `schema/edge.schema.json` to have a clear enum for valid types (not confirmed — must be verified).  

### 3B — Orphan / Unreachable Node Detection

**Gap classification:** Category C (GOVERNANCE_GAP_CLASSIFICATION.md Gap 5)  
**Evidence:** No in-degree/out-degree analysis exists anywhere.  
**Implementation:** New script or inline step. Computes in-degree for all nodes. Reports nodes with in-degree = 0 that are not designated roots. Optionally reports out-degree = 0 (sink) nodes.  
**CI impact:** Blocks PRs that introduce isolated nodes with no graph connections.  
**Risk:** Medium. Need to define what constitutes a legitimate root node vs. an orphan. Risk of false positives on intentionally isolated entry-point skills.  

---

## Tier 4 — New Governance Features

Beyond the scope of INITIATIVE-007R. Documented for future planning only.

- **Graph Health Score as CI artifact** — publish structured JSON score per PR
- **Learning path depth metrics** — average/max depth reports
- **Tag population enforcement** — block skill PRs where `tags: []`
- **Recommendation benchmarking** — regression tests against known good goal→path pairs

---

## Execution Order Recommendation

Based on leverage and dependency ordering:

| Order | Item | Tier | Dependency | Expected CI Gain |
|---|---|---|---|---|
| 1 | 1A — Dangling Target Detection | 1 | None | Blocks dangling REQUIRES targets |
| 2 | 1B — Duplicate Edge Detection | 1 | None | Blocks redundant edges |
| 3 | 2A — Cycle Detection fix + CI | 2 | None | Blocks cycle introduction |
| 4 | 2B — Learning Path Validation | 2 | 2A | Blocks broken learning paths |
| 5 | 3A — Invalid Edge Type Detection | 3 | None | Blocks misspelled edge types |
| 6 | 3B — Orphan Detection | 3 | None | Blocks isolated nodes |
| 7 | 1C — Quality Score PR Gate | 1 | Confirm quality_score.py | Blocks quality regressions |
| 8 | 2C — Recommendation Score Threshold | 2 | None | Improves runtime quality |

Items 1 and 2 should be implemented first: they are the fastest to implement, have zero risk, and close the most critical gap (dangling targets are the most likely failure mode as the graph grows).

---

*No synthetic metrics. No inferred relationships. All findings traceable to direct file reads.*
