# REQUIRES_IMPACT_ANALYSIS.md
**Mission:** INITIATIVE-002A — Phase 5
**Date:** 2026-06-22
**Measured values only. No invented metrics.**

All quantitative inputs sourced from `meta/INITIATIVE_001C_AUDIT_REPORT.md` (367 nodes, 773 edges).

---

## Input Measurements (All from INITIATIVE_001C)

| Metric | Measured Value | Source |
|---|---|---|
| Total nodes | 367 | INITIATIVE_001C pre-flight |
| Total edges | 773 | INITIATIVE_001C pre-flight |
| REQUIRES edges | **0** | INITIATIVE_001C edge type distribution |
| Orphan nodes | **54** | INITIATIVE_001C Phase 3 |
| Sink nodes (out_degree=0) | 88 | INITIATIVE_001C Phase 4 |
| Source nodes (in_degree=0) | 112 | INITIATIVE_001C Phase 4 |
| Dangling target edges | 9 | INITIATIVE_001C schema validation |
| `recommend.py` dependency BFS | BLOCKED (no REQUIRES) | INITIATIVE_001C Phase 5 |
| `recommend.py` learning path sort | BLOCKED (no REQUIRES) | INITIATIVE_001C Phase 5 |

---

## Impact Estimate: Orphan Node Connectivity

**Measured:** 54 orphan nodes have zero edges.

**Observed from 2-file sample:** LEVEL 3 patterns yield ~2.5 REQUIRES candidates per file.
Pilot extracted 5 candidates from 2 files. Target nodes in pilot: Plan-and-Execute, ReAct.

**Orphan reduction estimate:**
- Cannot be precisely calculated without reading all 54 orphan skill files.
- Lower bound provable: C-005 targets `react-pattern`; if it is orphaned, adding that edge resolves 1.
- Upper bound: UNKNOWN — requires reading all 54 orphan files.

| Estimate Type | Value | Basis |
|---|---|---|
| Lower bound (proven from pilot) | 0–1 orphans resolved | C-005 targets a known dangling node |
| Upper bound | UNKNOWN | Not enough files read |

---

## Impact Estimate: `recommend.py` Behavior Change

Current state (INITIATIVE_001C confirmed):
- `recommend.py` backward BFS on REQUIRES: **BLOCKED** — returns empty path for all queries.
- Learning path generation (topological sort): **BLOCKED**.

With pilot candidates (4 ready, 1 deferred):

| Capability | Before | After (pilot only) | After (full extraction) |
|---|---|---|---|
| Learning path for `plan-and-execute` | BLOCKED | 2-step path available | UNKNOWN |
| Dependency resolution | BLOCKED | 4–5 edges traversable | UNKNOWN |
| Topological sort | BLOCKED | Partial (connected component only) | UNKNOWN |

---

## Impact Estimate: Dangling Reference Resolution

**Measured:** 9 dangling target edges in INITIATIVE_001C.

REQUIRES edge addition does not directly resolve dangling edges — that is a node ID alignment
issue (blocker B-005 in INITIATIVE_001C). However, INITIATIVE-002B extraction will force
reading the affected files, which surfaces the correct slug discrepancy for repair.

**Estimated dangling edges resolvable as side-effect of INITIATIVE-002B reading:** up to 9.
(Not guaranteed — depends on whether extraction covers those specific files.)

---

## Summary

| Impact Dimension | Measured Baseline | Expected Change | Certainty |
|---|---|---|---|
| REQUIRES edges | 0 | +4 minimum (pilot ready candidates) | HIGH |
| Orphan nodes resolved | 54 | 0–1 (pilot scope) | LOW |
| Learning paths unlocked | 0 | ≥1 (goal-decomp → planning-decomp → plan-execute) | MEDIUM |
| Dangling edges resolved | 9 | 0 (separate issue) | HIGH |
| `recommend.py` BFS unblocked | BLOCKED | Partially unblocked | MEDIUM |
