# NEXT_TASK_RECOMMENDATION.md

> Generated: 2026-06-21 — Governance Reconciliation Phase 4  
> Based on measured graph state: 47 nodes, 93 edges, schema 1.3  
> No graph modifications performed to generate this document.

---

## Current Bottlenecks (from graph evidence)

| Bottleneck | Impact | Severity |
|---|---|---|
| `01-perception` has 0 nodes | Blocks G03 (Browser Agent), G05, G06 | HIGH |
| TASK-002 not executed | Context engineering gap; 5 nodes missing from `02-reasoning` | HIGH |
| `06-knowledge` has 0 nodes | Blocks G02, G04 | MEDIUM |
| `08-planning` has 0 nodes | Blocks G06, G08 | MEDIUM |
| Phase 1 incomplete (47/53 nodes) | All Phase 2 tasks blocked | MEDIUM |

---

## Task Ranking (by graph impact)

| Rank | Task | Nodes | Edges | Unblocks | Dependencies |
|---|---|---|---|---|---|
| **1** | **TASK-002** — Context Engineering | +5 | +10–12 | Phase 1 progress, closes reasoning gap | None |
| **2** | **TASK-004** — Causal + Counterfactual | +3 | +6–8 | `02-reasoning` saturation, deeper reasoning paths | TASK-003 ✅ |
| **3** | **TASK-005** — Core Perception | +6 | +12–15 | G03, G05, G06; unlocks TASK-006 | None |
| 4 | TASK-006 — Document/Data Perception | +9 | +15–18 | `01-perception` depth | TASK-005 |

---

## Recommended Next Task: TASK-002

**Why TASK-002 over TASK-004:**
- TASK-002 adds 5 nodes vs TASK-004's 3 — greater Phase 1 progress per execution
- TASK-002 connects to hub `skill:prompt-engineering` (centrality 0.2391) with multiple new REQUIRES edges, increasing graph connectivity more than TASK-004
- TASK-002 has zero dependencies; TASK-004 depends on TASK-003 (already done, but TASK-002 was sequenced before TASK-004 in the original backlog)

**Why not TASK-005 first:**
- TASK-005 (perception) is higher strategic impact (unlocks 3 goals) but TASK-002 (context engineering) is a foundational gap that affects recommendation quality immediately
- TASK-002 completes `02-reasoning` saturation target; TASK-005 adds a new category
- Either ordering is valid — operator may choose TASK-005 if goal coverage is the priority

---

## Post-TASK-002 State (projected from backlog spec)

| Metric | Current | After TASK-002 |
|---|---|---|
| Nodes | 47 | ~52 |
| Edges | 93 | ~103–105 |
| Phase 1 completion | 88.7% | ~98% |
| `02-reasoning` nodes | 10 | ~15 |

---

*Recommendation version: 1.0.0 — 2026-06-21*
