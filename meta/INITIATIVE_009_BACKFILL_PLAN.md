# INITIATIVE-009 BACKFILL PLAN

**Date:** 2026-06-23  
**Phase:** 3  
**Scope:** Frontmatter `prerequisites:` additions only. No body text modifications.

---

## Rule

Only `prerequisites:` frontmatter additions. Do not modify body text. Do not remove existing frontmatter fields.

---

## Approved Additions

### C-002: agentic-rag → react (new addition)

**File:** `skills/09-agentic-patterns/agentic-rag.md`  
**Current prerequisites:**
```yaml
prerequisites:
  - 03-memory/rag
```
**Proposed prerequisites:**
```yaml
prerequisites:
  - 03-memory/rag
  - 09-agentic-patterns/react
```
**Evidence source:** `agentic-rag.md` Related Skills section lists `[ReAct](react.md)` with directional language confirming react is used within the agentic RAG loop.  
**Confidence:** 0.80

---

### C-004: planning-decomposition → goal-decomposition

**File:** `skills/02-reasoning/planning-decomposition.md`  
**Current prerequisites:** none  
**Proposed prerequisites:**
```yaml
prerequisites:
  - 02-reasoning/goal-decomposition
```
**Evidence source:** `planning-decomposition.md` Related Skills: "[Goal Decomposition](goal-decomposition.md) — operates at intent level; precedes planning decomposition"  
**Confidence:** 0.90

---

### C-005: planning-decomposition → react

**File:** `skills/02-reasoning/planning-decomposition.md`  
**Current prerequisites:** none (adding alongside C-004)  
**Proposed prerequisites:**
```yaml
prerequisites:
  - 02-reasoning/goal-decomposition
  - 09-agentic-patterns/react
```
**Evidence source:** `planning-decomposition.md` Related Skills: "[ReAct Pattern](../09-agentic-patterns/react-pattern.md) — executes individual plan steps"  
**Confidence:** 0.82

---

### C-007: goal-decomposition → planning-decomposition

**File:** `skills/02-reasoning/goal-decomposition.md`  
**Current prerequisites:** none  
**Proposed prerequisites:**
```yaml
prerequisites:
  - 02-reasoning/planning-decomposition
```
**Evidence source:** `goal-decomposition.md` body explicitly states Planning Decomposition "converts sub-goals into executable tasks" — establishes that goal-decomp is understood in context of what comes after it.  

⚠️ **Cycle check:** `planning-decomposition → goal-decomposition` (C-004) + `goal-decomposition → planning-decomposition` (C-007) = **CYCLE DETECTED**.

**Decision:** REJECT C-007. The directional relationship is: goal-decomposition PRECEDES planning-decomposition. Therefore only C-004 is added (planning-decomp requires goal-decomp). C-007 is dropped.

---

### C-006: goal-decomposition → plan-and-execute (DEFERRED)

**File:** `skills/02-reasoning/goal-decomposition.md`  
**Rationale for deferral:** Adding `prerequisites: - 09-agentic-patterns/plan-and-execute` on `goal-decomposition` creates a cross-category dependency where an intermediate reasoning skill requires an advanced agentic pattern. This is architecturally inverted — plan-and-execute should depend on goal-decomposition, not the reverse. **REJECT in this direction.**

**Correct direction (added as C-006-REV):** `plan-and-execute` should gain `02-reasoning/goal-decomposition` as prerequisite (already covered by plan-and-execute's existing `react` prerequisite chain; low priority).

---

## Final Approved Frontmatter Changes

| Candidate | File | Addition | Status |
|-----------|------|----------|--------|
| C-002 | `09-agentic-patterns/agentic-rag.md` | `09-agentic-patterns/react` | ✅ APPROVED |
| C-004 | `02-reasoning/planning-decomposition.md` | `02-reasoning/goal-decomposition` | ✅ APPROVED |
| C-005 | `02-reasoning/planning-decomposition.md` | `09-agentic-patterns/react` | ✅ APPROVED |
| C-007 | `02-reasoning/goal-decomposition.md` | `02-reasoning/planning-decomposition` | ❌ REJECTED (cycle) |
| C-006 | `02-reasoning/goal-decomposition.md` | `09-agentic-patterns/plan-and-execute` | ❌ REJECTED (inverted) |
| C-001 | `09-agentic-patterns/rag.md` | `09-agentic-patterns/cot` | ⚠️ DEFERRED (confidence 0.72, needs body review) |
| C-003 | `09-agentic-patterns/plan-and-execute.md` | `02-reasoning/planning-decomposition` | ✅ APPROVED |
| C-008 | `09-agentic-patterns/rag.md` | `03-memory/memory-injection` | ⚠️ DEFERRED (cross-category, needs `03-memory/memory-injection` node existence check) |

**Net new REQUIRES edges from this plan:** 4  
**REQUIRES total after:** 9 + 4 = 13  

⚠️ **Gap vs target:** Target is ≥ 50. Gap = 37 additional REQUIRES edges needed.  
This plan represents the evidence available from the files read in this session. Categories `07-tool-use`, `06-frameworks`, `12-evaluation`, and the full `03-memory` catalog require additional file reads in **INITIATIVE-009B**.

---

**Status:** COMPLETE (partial — see gap note)
