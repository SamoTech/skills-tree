# INITIATIVE-009 RECOMMENDATION BENCHMARK

**Date:** 2026-06-23  
**Phase:** 5  
**Method:** Path depth and prerequisite chain analysis from confirmed frontmatter evidence

---

## Benchmark Skills

### 1. react

**Confirmed prerequisite chain:**
```
react
  └── requires: cot
```

| Metric | Before | After (no change — react already has prereq) |
|--------|--------|----------------------------------------------|
| Path depth | 1 | 1 |
| Reachable prerequisites | 1 (`cot`) | 1 |
| Dependency coverage | Partial | Partial |

**Recommendation usefulness:** A learner querying `react` gets `cot` as prerequisite — useful. No change from this initiative.

---

### 2. plan-and-execute

**Confirmed prerequisite chain BEFORE:**
```
plan-and-execute
  └── requires: react
        └── requires: cot
```
Path depth: 2, Reachable prereqs: 2

**Confirmed prerequisite chain AFTER (C-003 applied):**
```
plan-and-execute
  ├── requires: react
  │     └── requires: cot
  └── requires: planning-decomposition  [NEW]
        └── requires: goal-decomposition  [NEW]
```
Path depth: 3, Reachable prereqs: 4

| Metric | Before | After |
|--------|--------|-------|
| Path depth | 2 | 3 |
| Reachable prerequisites | 2 | 4 |
| Dependency coverage | Low | Medium |

**Recommendation usefulness:** Significant improvement. A learner querying `plan-and-execute` now receives a complete learning path: goal-decomposition → planning-decomposition → react + cot → plan-and-execute.

---

### 3. lats

**Confirmed prerequisite chain (unchanged by this initiative):**
```
lats
  ├── requires: react
  │     └── requires: cot
  ├── requires: tot
  │     └── requires: cot
  └── requires: reflection
        └── requires: cot
```
Path depth: 2, Reachable prereqs: 4

**Recommendation usefulness:** Already well-covered. LATS is the deepest dependency chain in the graph at baseline.

---

### 4. rag (09-agentic-patterns)

**Confirmed prerequisite chain BEFORE:** None (0 prerequisites in frontmatter)  
**Confirmed prerequisite chain AFTER:** C-001 deferred (confidence 0.72, below threshold for this initiative's committed changes)

| Metric | Before | After |
|--------|--------|-------|
| Path depth | 0 | 0 |
| Reachable prerequisites | 0 | 0 |

**Recommendation usefulness:** No change. C-001 deferred to INITIATIVE-009B after body text review.

---

### 5. agentic-rag

**Confirmed prerequisite chain BEFORE:**
```
agentic-rag
  └── requires: 03-memory/rag
```
Path depth: 1, Reachable prereqs: 1

**Confirmed prerequisite chain AFTER (C-002 applied):**
```
agentic-rag
  ├── requires: 03-memory/rag
  └── requires: react  [NEW]
        └── requires: cot
```
Path depth: 2, Reachable prereqs: 3

| Metric | Before | After |
|--------|--------|-------|
| Path depth | 1 | 2 |
| Reachable prerequisites | 1 | 3 |
| Dependency coverage | Low | Medium |

**Recommendation usefulness:** Meaningful improvement. Learner querying `agentic-rag` now receives both retrieval foundation (`03-memory/rag`) and agent architecture foundation (`react` → `cot`).

---

## Benchmark Summary

| Skill | Prereqs Before | Prereqs After | Delta |
|-------|---------------|---------------|-------|
| `react` | 1 | 1 | 0 |
| `plan-and-execute` | 2 | 4 | +2 |
| `lats` | 4 | 4 | 0 |
| `rag` | 0 | 0 | 0 |
| `agentic-rag` | 1 | 3 | +2 |

**Average reachable prerequisites:** Before: 1.6 → After: 2.4 (+50%)  
**Recommendation depth improvement:** Meaningful for `plan-and-execute` and `agentic-rag`.

---

**Status:** COMPLETE
