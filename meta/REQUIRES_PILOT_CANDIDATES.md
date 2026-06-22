# REQUIRES_PILOT_CANDIDATES.md
**Mission:** INITIATIVE-002A — Phase 4
**Date:** 2026-06-22
**Constraint:** Only candidates from files read in this session. No inference. No invention.
**Files read:** `skills/02-reasoning/least-to-most.md`, `skills/02-reasoning/planning-decomposition.md`
**Candidates generated:** 5 (LEVEL 3 evidence only)

> The 50-candidate maximum cannot be reached from 2 source files alone.
> Remaining capacity (45 slots) requires reading additional skill files in INITIATIVE-002B.

---

## Candidate Edges

### C-001
| Field | Value |
|---|---|
| **Source** | `02-reasoning/chain-of-thought` |
| **Target** | `02-reasoning/least-to-most` |
| **Type** | REQUIRES |
| **Evidence text** | "Least-to-Most **extends** CoT with explicit decomposition" |
| **Source file** | `skills/02-reasoning/least-to-most.md` → `## Related Skills` |
| **Confidence level** | LEVEL 3 |
| **Edge direction rationale** | "extends" → CoT is the prerequisite; Least-to-Most builds on top of it |
| **Review flag** | ⚠️ REQUIRES HUMAN REVIEW |
| **Target node exists in graph?** | UNKNOWN — `02-reasoning/chain-of-thought` slug not verified against graph IDs |

---

### C-002
| Field | Value |
|---|---|
| **Source** | `02-reasoning/least-to-most` |
| **Target** | `09-agentic-patterns/plan-and-execute` |
| **Type** | REQUIRES |
| **Evidence text** | "the agentic pattern **built on** this reasoning approach" |
| **Source file** | `skills/02-reasoning/least-to-most.md` → `## Related Skills` |
| **Confidence level** | LEVEL 3 |
| **Edge direction rationale** | "built on" → Least-to-Most is prerequisite; Plan-and-Execute builds on top of it |
| **Review flag** | ⚠️ REQUIRES HUMAN REVIEW |
| **Target node exists in graph?** | UNKNOWN — `09-agentic-patterns/plan-and-execute` not verified against graph IDs |

---

### C-003
| Field | Value |
|---|---|
| **Source** | `02-reasoning/planning-decomposition` |
| **Target** | `09-agentic-patterns/plan-and-execute` |
| **Type** | REQUIRES |
| **Evidence text** | "the agentic pattern that **executes** decomposed plans" |
| **Source file** | `skills/02-reasoning/planning-decomposition.md` → `## Related Skills` |
| **Confidence level** | LEVEL 3 |
| **Edge direction rationale** | "executes plans from" → Planning Decomposition is prerequisite; Plan-and-Execute consumes its output |
| **Review flag** | ⚠️ REQUIRES HUMAN REVIEW |
| **Target node exists in graph?** | UNKNOWN — same slug issue as C-002 |

---

### C-004
| Field | Value |
|---|---|
| **Source** | `02-reasoning/goal-decomposition` |
| **Target** | `02-reasoning/planning-decomposition` |
| **Type** | REQUIRES |
| **Evidence text** | "**operates at intent level; precedes** planning decomposition" |
| **Source file** | `skills/02-reasoning/planning-decomposition.md` → `## Related Skills` |
| **Confidence level** | LEVEL 3 |
| **Edge direction rationale** | "precedes" — explicit ordering; Goal Decomposition precedes Planning Decomposition |
| **Review flag** | ⚠️ REQUIRES HUMAN REVIEW |
| **Target node exists in graph?** | UNKNOWN — slug format TBC |

---

### C-005
| Field | Value |
|---|---|
| **Source** | `02-reasoning/planning-decomposition` |
| **Target** | `09-agentic-patterns/react-pattern` |
| **Type** | REQUIRES |
| **Evidence text** | "**executes individual plan steps**" |
| **Source file** | `skills/02-reasoning/planning-decomposition.md` → `## Related Skills` |
| **Confidence level** | LEVEL 3 |
| **Edge direction rationale** | ReAct executes steps produced by Planning Decomposition → dependency |
| **Review flag** | ⚠️ REQUIRES HUMAN REVIEW |
| **Target node exists in graph?** | ⚠️ DANGLING — INITIATIVE_001C confirmed `09-agentic-patterns/react-pattern` is a dangling target (not registered in graph); edge DEFERRED until node slug resolved |

---

## Summary

| Candidates | Count |
|---|---|
| Total generated | 5 |
| LEVEL 1 | 0 |
| LEVEL 2 | 0 |
| LEVEL 3 | 5 |
| Deferred (dangling target) | 1 (C-005) |
| Ready for graph write (pending node ID verification) | 4 |
| Remaining capacity to 50-candidate limit | 45 |

## Blocker

Node ID slug format must be verified before writing any candidate.
Example: graph uses `02-reasoning/least-to-most` or `skill:least-to-most` or `least-to-most`?
This cannot be determined without reading `data/SKILLS_GRAPH.json` node list directly.
**Action for INITIATIVE-002B:** Read graph node IDs first; re-verify all 4 ready candidates.
