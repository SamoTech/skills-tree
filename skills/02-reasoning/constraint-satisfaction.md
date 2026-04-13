---
title: "Constraint Satisfaction"
category: 02-reasoning
level: advanced
stability: stable
description: "Apply constraint satisfaction in AI agent workflows."
added: "2025-03"
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-02-reasoning-constraint-satisfaction.json)

# Constraint Satisfaction

**Category:** `reasoning`  
**Skill Level:** `advanced`  
**Stability:** `stable`  
**Added:** 2025-03  
**Version:** v2

---

## Description

Find values for a set of variables that simultaneously satisfy all given constraints. CSP reasoning is used in scheduling, configuration, planning, and any task where multiple hard requirements must hold at once.

---

## Formal Definition

A CSP has three components:
- **Variables** `X = {X₁, X₂, ..., Xₙ}` — what we are assigning values to
- **Domains** `D = {D₁, D₂, ..., Dₙ}` — possible values per variable
- **Constraints** `C` — restrictions on combinations of variable assignments

A **solution** is an assignment where every variable has a value from its domain and every constraint is satisfied.

---

## Example — Meeting Scheduler

```
Variables:  Alice_slot, Bob_slot, Carol_slot
Domains:    {Mon9, Mon10, Mon11, Tue9, Tue10}
Constraints:
  - All three must share the same slot (meeting constraint)
  - Alice unavailable Mon9, Mon10
  - Bob unavailable Tue10
  - Carol unavailable Mon11

Backtrack search:
  Try Mon9  → Alice fails ✗
  Try Mon10 → Alice fails ✗
  Try Mon11 → Carol fails ✗
  Try Tue9  → All available ✓  → SOLUTION: Tue9
```

---

## Solving Strategies

| Strategy | When to Use | Complexity |
|---|---|---|
| Backtracking search | Small/medium domains | Exponential worst-case |
| Arc consistency (AC-3) | Reduce domains before search | O(ed³) |
| Forward checking | Prune as you assign | Polynomial per step |
| LP/MIP solvers | Numeric constraints | Polynomial (LP) |
| SAT solvers | Boolean constraints | NP-complete, fast heuristics |

---

## Python Example (python-constraint)

```python
from constraint import Problem

problem = Problem()
problem.addVariables(["Alice", "Bob", "Carol"],
                     ["Mon9","Mon10","Mon11","Tue9","Tue10"])

# All must meet at same time
problem.addConstraint(lambda a, b, c: a == b == c, ["Alice", "Bob", "Carol"])
# Individual unavailabilities
problem.addConstraint(lambda a: a not in ["Mon9", "Mon10"], ["Alice"])
problem.addConstraint(lambda b: b != "Tue10", ["Bob"])
problem.addConstraint(lambda c: c != "Mon11", ["Carol"])

solutions = problem.getSolutions()
print(solutions)  # [{'Alice': 'Tue9', 'Bob': 'Tue9', 'Carol': 'Tue9'}]
```

---

## LLM Prompt Pattern

```
Variables: [list each variable]
Domains:   [list valid values per variable]
Constraints:
  1. [constraint 1]
  2. [constraint 2]
  ...

Find an assignment satisfying ALL constraints.
Show your work: for each candidate, check each constraint.
If no solution exists, explain which constraints conflict.
```

---

## Related Skills

- [Planning](planning.md)
- [Mathematical Reasoning](mathematical-reasoning.md)
- [Decision Making](decision-making.md)
- [Task Decomposition](task-decomposition.md)
