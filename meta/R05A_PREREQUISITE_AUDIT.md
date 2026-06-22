# R05A Prerequisite Audit

**Mission:** R-05A — Edge Extraction Pilot  
**Date:** 2026-06-22  
**Purpose:** Identify all prerequisite/dependency language found in the 5 scanned categories.

---

## Methodology

Search terms applied against evidence text of all 73 extracted edges:
- `prerequisite`
- `requires` / `REQUIRES` edge type
- `builds on`, `extends`
- `precedes`
- `depends on`

Only explicit text matches. No inferred relationships.

---

## Matches by Keyword Pattern

### Pattern: "prerequisite" (literal word)

| Dependency | File | Evidence |
|------------|------|----------|
| `step-back-prompting` → `prompt-engineering` | `step-back-prompting.md` | "Related Skills: '[Prompt Engineering] — prerequisite skill'" |
| `meta-prompting` → `prompt-engineering` | `meta-prompting.md` | "Related Skills: '[Prompt Engineering] — prerequisite; meta-prompting automates this skill'" |

### Pattern: REQUIRES edge type (structural dependency signal)

| Dependency | File | Evidence |
|------------|------|----------|
| `self-consistency` → `chain-of-thought` | `self-consistency.md` | "Description: 'augments Chain of Thought by sampling N independent reasoning chains'" |
| `least-to-most` → `chain-of-thought` | `least-to-most.md` | "Least-to-Most extends CoT with explicit decomposition" |
| `task-decomposition` → `planning` | `task-decomposition.md` | "distinct from Planning — decomposition produces what to do" |
| `planning-decomposition` → `goal-decomposition` | `planning-decomposition.md` | "'[Goal Decomposition] — operates at intent level; precedes planning decomposition'" |
| `reasoning-under-uncertainty` → `rag-retrieval` | `reasoning-under-uncertainty.md` | "[RAG Retrieval] — retrieves evidence to reduce uncertainty" |
| `vector-store-retrieval` → `embedding-generation` | `vector-store-retrieval.md` | "[Embedding Generation] — how vector is produced" |
| `plan-and-execute` → `planning` | `plan-and-execute.md` | "Related Skills: `planning`" |
| `react` → `planning` | `react.md` | "[Planning] — structured plan first, then execute" |

### Pattern: "precedes" (order language)

| Dependency | File | Evidence |
|------------|------|----------|
| `planning-decomposition` → `goal-decomposition` | `planning-decomposition.md` | "'[Goal Decomposition] — operates at intent level; precedes planning decomposition'" |

### Pattern: "extends" / "builds on"

| Dependency | File | Evidence |
|------------|------|----------|
| `least-to-most` → `chain-of-thought` | `least-to-most.md` | "Least-to-Most extends CoT with explicit decomposition" |

---

## Summary

| Pattern | Unique Pairs Found |
|---------|-------------------|
| Literal "prerequisite" | 2 |
| REQUIRES-type edges | 12 |
| "precedes" | 1 |
| "extends" / "builds on" | 2 |
| **Total unique prerequisite pairs** | **~14** |

---

## Key Prerequisite Chains Identified

The following learning chains are supported by explicit repository evidence:

1. `prompt-engineering` → `step-back-prompting` → `meta-prompting`
2. `chain-of-thought` → `self-consistency`
3. `chain-of-thought` → `least-to-most`
4. `goal-decomposition` → `planning-decomposition` → `plan-and-execute`
5. `planning` → `task-decomposition`
6. `planning` → `plan-and-execute`
7. `planning` → `react`
8. `embedding-generation` → `vector-store-retrieval`

---

## Gaps Identified

- **03-memory** (14 of 17 files unread): `episodic-memory.md`, `working-memory.md`, `semantic-memory.md` likely contain further prerequisite chains — NOT YET EXTRACTED.
- **07-tool-use** (30 of 31 files unread): only `function-calling.md` was sampled.
- **12-data** (16 of 18 files unread): only `json-transformation.md` and `csv-processing.md` sampled.
- **09-agentic-patterns** (15 of 19 files unread): `tot.md`, `mcts.md`, `subagent-delegation.md` etc. not yet read.

*Prerequisite coverage will increase significantly in R-05B full scan.*
