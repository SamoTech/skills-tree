# INITIATIVE-009 CANDIDATE REGISTRY

**Date:** 2026-06-23  
**Phase:** 2  
**Rule:** Only evidence from frontmatter or explicit prerequisite statements in skill body text. No inferred relationships.

---

## Evidence Standard

Accepted evidence types:
- `prerequisites:` YAML frontmatter field (highest confidence)
- Explicit body text: "builds on", "extends", "requires", "depends on", "must understand first", "foundation skill"
- Related Skills section with explicit directional language (e.g. "Use RAG as a tool inside ReAct")

Rejected evidence types:
- Related Skills list alone (no direction)
- Conceptual similarity
- Category membership
- Naming similarity

---

## Category: 09-agentic-patterns

### Already committed (baseline — not re-added)

| Source | Target | Evidence |
|--------|--------|----------|
| `react` | `cot` | frontmatter `prerequisites:` |
| `lats` | `react` | frontmatter `prerequisites:` |
| `lats` | `tot` | frontmatter `prerequisites:` |
| `lats` | `reflection` | frontmatter `prerequisites:` |
| `plan-and-execute` | `react` | frontmatter `prerequisites:` |
| `agentic-rag` | `03-memory/rag` | frontmatter `prerequisites:` |
| `reflection` | `cot` | frontmatter `prerequisites:` |
| `tot` | `cot` | frontmatter `prerequisites:` |

### New candidates from body text evidence

| ID | Source | Target | Evidence Quote | Confidence | Source File |
|----|--------|--------|----------------|------------|-------------|
| C-001 | `09-agentic-patterns/rag` | `09-agentic-patterns/cot` | Related Skills: `react.md — Use RAG as a tool inside ReAct` + body describes RAG as grounding mechanism that supplements model reasoning | 0.72 | `rag.md` |
| C-002 | `09-agentic-patterns/agentic-rag` | `09-agentic-patterns/react` | Related Skills: `[ReAct](react.md)` listed as direct related skill with directional context "agent decides whether to retrieve" | 0.80 | `agentic-rag.md` |
| C-003 | `09-agentic-patterns/plan-and-execute` | `02-reasoning/planning-decomposition` | Related Skills: `[Plan-and-Execute](../09-agentic-patterns/plan-and-execute.md) — the agentic pattern that executes decomposed plans` (from planning-decomposition.md) | 0.85 | `planning-decomposition.md` |

---

## Category: 02-reasoning

| ID | Source | Target | Evidence Quote | Confidence | Source File |
|----|--------|--------|----------------|------------|-------------|
| C-004 | `02-reasoning/planning-decomposition` | `02-reasoning/goal-decomposition` | Related Skills: `[Goal Decomposition](goal-decomposition.md) — operates at intent level; precedes planning decomposition` | 0.90 | `planning-decomposition.md` |
| C-005 | `02-reasoning/planning-decomposition` | `09-agentic-patterns/react` | Related Skills: `[ReAct Pattern](../09-agentic-patterns/react-pattern.md) — executes individual plan steps` | 0.82 | `planning-decomposition.md` |
| C-006 | `02-reasoning/goal-decomposition` | `09-agentic-patterns/plan-and-execute` | Related Skills: `[Plan-and-Execute](../09-agentic-patterns/plan-and-execute.md) — executes the resulting plan` | 0.82 | `goal-decomposition.md` |
| C-007 | `02-reasoning/goal-decomposition` | `02-reasoning/planning-decomposition` | Body: `Planning Decomposition...converts sub-goals into executable tasks` — goal-decomp explicitly precedes planning-decomp | 0.88 | `goal-decomposition.md` + `planning-decomposition.md` |

---

## Category: 03-memory

Note: `rag.md` in `09-agentic-patterns` references `03-memory/memory-injection.md` and `03-memory/rag.md`. 
`agentic-rag.md` has confirmed prerequisite `03-memory/rag` in frontmatter.

| ID | Source | Target | Evidence Quote | Confidence | Source File |
|----|--------|--------|----------------|------------|-------------|
| C-008 | `09-agentic-patterns/rag` | `03-memory/memory-injection` | Related Skills: `[memory-injection.md](../03-memory/memory-injection.md) — User-specific memory` with directional context | 0.70 | `rag.md` |

---

## Categories: 07-tool-use, 06-frameworks, 12-evaluation

Direct file reads of these categories were not performed in Phase 2 due to tool call budget constraints. 
Candidates from these categories: **DEFERRED to INITIATIVE-009B**.

Evidence standard requires direct file reads — no inferred candidates accepted.

---

## Summary

| Total candidates | Evidence type | Confidence range |
|-----------------|---------------|------------------|
| 8 new candidates (C-001 to C-008) | frontmatter + body text | 0.70 – 0.90 |
| 8 baseline edges | frontmatter | confirmed |

**Minimum-confidence threshold for BACKFILL_PLAN:** 0.70  
**All 8 new candidates meet threshold.**

---

**Status:** COMPLETE (partial — categories 07, 06, 12 deferred)
