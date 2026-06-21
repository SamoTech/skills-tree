# AGENT_SKILLS_MASTER_PLAN.md — Authoritative Execution Plan

> Rebuilt from repository evidence on 2026-06-21.  
> All values measured from `data/SKILLS_GRAPH.json` and confirmed reports.  
> No estimates. No projected values. UNKNOWN used where evidence is absent.

---

## Graph State (measured)

| Metric | Value |
|---|---|
| Total nodes | 47 |
| Total edges | 93 |
| Schema version | 1.3 |
| Categories with ≥1 node | 10 |
| Categories with 0 nodes | 5 (`01-perception`, `06-knowledge`, `08-planning`, `13-execution`, `14-evaluation`) |

---

## Phase Structure

### Phase 1 — Core Agent Skills
**Target:** 53 nodes (currently 47 — need +6 minimum)  
**Status:** IN PROGRESS — 88.7% complete

Phase 1 must cover:
- `02-reasoning` ✅ (10 nodes — TASK-003 DONE)
- `09-agentic-patterns` ✅ (24 nodes — TASK-001 DONE)
- `01-perception` ❌ (0 nodes — TASK-005 required)

Phase 1 is **not complete** until `01-perception` has at least 6 nodes.

### Phase 2+
Blocked until Phase 1 completes. See `meta/AGENT_SKILLS_BACKLOG.md` for full list.

---

## Task Execution Order (Phase 1)

| Priority | Task ID | Title | Status | Nodes | Dependencies |
|---|---|---|---|---|---|
| 1 | TASK-002 | Context Engineering skills | **OPEN** | +5 | None |
| 2 | TASK-004 | Causal + counterfactual reasoning | **OPEN** | +3 | TASK-003 ✅ |
| 3 | TASK-005 | Core perception skills | **OPEN** | +6 | None |
| 4 | TASK-006 | Document/data perception | **BLOCKED** | +9 | TASK-005 |

**Next to execute:** TASK-002 (highest value, no dependencies, closes context engineering gap)

---

## Category Coverage Matrix

| Category | Nodes | Phase 1 Target | Gap |
|---|---|---|---|
| `01-perception` | 0 | 6 | **-6** |
| `02-reasoning` | 10 | 10 | 0 ✅ |
| `03-memory` | 4 | 4 | 0 ✅ |
| `04-action-execution` | 1 | 1 | 0 ✅ |
| `05-code` | 1 | UNKNOWN | — |
| `06-knowledge` | 0 | UNKNOWN | — |
| `07-tool-use` | 2 | UNKNOWN | — |
| `08-planning` | 0 | UNKNOWN | — |
| `09-agentic-patterns` | 24 | 24 | 0 ✅ |
| `10-computer-use` | 1 | UNKNOWN | — |
| `11-web` | 1 | UNKNOWN | — |
| `12-data` | 1 | UNKNOWN | — |
| `13-execution` | 0 | UNKNOWN | — |
| `14-evaluation` | 0 | UNKNOWN | — |
| `15-orchestration` | 2 | UNKNOWN | — |

---

## Bottlenecks

1. **`01-perception` has 0 nodes** — blocks G03 (Browser Agent), G05, G06. TASK-005 is the unlock.
2. **TASK-002 not yet executed** — context engineering is a foundational gap; `skill:context-management` covers working memory only, not context window optimization.
3. **Phase 2 fully blocked** — 53-node threshold not yet reached; no Phase 2 task should be executed.

---

## Hub Nodes (leverage points for graph recommendations)

| Node | In-Degree | Out-Degree | Centrality | Role |
|---|---|---|---|---|
| `skill:prompt-engineering` | 10 | 1 | 0.2391 | Primary foundation hub |
| `skill:cot` | 5 | 2 | 0.1522 | Reasoning hub |
| `skill:react-pattern` | 4 | 3 | 0.1522 | Agentic execution hub |
| `skill:llm-orchestration` | 7 | 0 | 0.1522 | Terminal orchestration hub |
| `skill:multi-agent-coordination` | 4 | 2 | 0.1304 | Coordination hub |

---

*Plan version: 2.0.0 — Rebuilt from graph evidence 2026-06-21*
