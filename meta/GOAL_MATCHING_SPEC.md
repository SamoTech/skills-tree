# GOAL_MATCHING_SPEC.md

**Initiative:** INITIATIVE-012C  
**Phase:** 2  
**Status:** COMPLETE

---

## Overview

The goal matching engine maps a user-selected goal to a ranked list of skills using only graph evidence. No LLM inference. Fully deterministic.

---

## Pipeline

```
Goal (id, title, categories, keywords)
  │
  ▼
Graph Node Scan
  │  Filter: node.category ∈ goal.categories
  │  Filter: node.category ≠ "00-sandbox"
  ▼
Candidate Skills
  │
  ▼
Prerequisite Expansion
  │  For each candidate: expand node.prerequisites recursively
  │  Add prereq nodes not already in candidate set
  ▼
Ranked Skill List
  │  Sort by: CAT_ORDER index → level weight (basic < intermediate < advanced)
  ▼
Blueprint Object
```

---

## Category Mapping

Each goal defines `categories: [primary, secondary, tertiary, ...]` in priority order.

The engine collects all nodes whose `category` appears in `goal.categories`.

---

## Level Weights

| Level | Weight |
|-------|--------|
| basic | 0 |
| intermediate | 1 |
| advanced | 2 |

Used for sorting within a category group and for computing aggregate difficulty.

---

## Difficulty Scoring

```
advRatio = count(level=advanced) / total_skills

if advRatio > 0.40  → difficulty = "advanced"
if advRatio > 0.15  → difficulty = "intermediate"
else                → difficulty = "beginner"
```

---

## Estimated Time

```
totalWeight = sum(levelWeight[skill.level] for skill in skills)
  where basic=0.5, intermediate=1, advanced=2

weeks = max(2, round(totalWeight * 0.8))
estimatedTime = "(weeks-1)–(weeks+2) weeks"
```

---

## Determinism Guarantee

- Input: goal.id (static)
- Graph source: SKILLS_GRAPH.json (static per commit)
- Sort: deterministic multi-key (CAT_ORDER index, level weight)
- Output: identical for same goal + same graph version

No randomness. No model calls. No external lookups.

---

_Generated: INITIATIVE-012C Phase 2_
