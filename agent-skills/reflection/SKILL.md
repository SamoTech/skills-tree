---
name: reflection
description: Add a structured critique-and-revision pass that evaluates an agent output against explicit criteria before acceptance.
metadata:
  source: skills/09-agentic-patterns/reflection.md
  category: 09-agentic-patterns
  version: "v2"
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-09-agentic-patterns-reflection.json)

# Reflection

**Category:** `agentic-patterns`
**Skill Level:** `advanced`
**Stability:** `stable`
**Added:** 2025-03

### Description

Add a structured critique-and-revision pass that evaluates an agent output against explicit criteria before acceptance. Reflection loops until the declared criteria pass or the iteration budget is spent; it is not independent evidence when the same model and context produce both draft and critique.

### Inputs / Outputs

| Direction | Field | Type | Contract |
|---|---|---|---|
| Input | draft | text | The output to critique and revise |
| Input | evaluation_criteria | list of object | Checkable acceptance criteria with a version |
| Output | revised_output | text | The final draft after the reflection passes |
| Output | reflection_log | list of object | Per-iteration findings and the changes made |

### Procedure
1. Declare the acceptance criteria and the iteration budget before the first pass.
2. Critique the draft against each criterion and cite the failing passage.
3. Revise the draft to address the findings; log the change per finding.
4. Stop when all criteria pass or the budget is spent; never iterate past the budget.
5. Verify the final draft against the declared criteria version.
6. Use external checks when the stakes require independence beyond same-model reflection.

### Example

```python
criteria = {'v1': ['cited', 'bounded']}
draft = {'text': '42 rows', 'cited': False, 'bounded': False}
budget = 3
for i in range(budget):
    fails = [c for c in criteria['v1'] if not draft[c]]
    if not fails: break
    draft = dict(draft, **{c: True for c in fails})
fails = [c for c in criteria['v1'] if not draft[c]]
assert fails == [] and draft['cited'] and draft['bounded']
print({'iterations': 1, 'status': 'accepted'})
```

### Related Skills

- [Critic Agent](critic-agent.md) - role-separated critique for independence
- [Self-Refine Critique Loop](self-refine-critique-loop.md) - the iterating variant
- [Tree of Thoughts](tot.md) - explore alternatives instead of revising one draft
- [Human-in-Loop](../14-security/human-in-loop.md) - external verification when stakes require it

## Failure Modes

- Same-model reflection presented as independent verification.
- Iterating past the declared budget or against shifting criteria.
- Accepting a draft whose criteria were never actually re-checked.
- Findings without cited passages, so revisions cannot be verified.

## Changelog
- v2 (2026-11): Structural modernization; added the input/output contract table, a skill-specific execution procedure, a deterministic example, and corpus-verified related links (replaced the unresolvable cross-category related references).
- v1 (2025-03): Initial entry.

## Evidence

- https://agentskills.io/specification

Evidence status: implementation guidance only; pattern behavior must be checked against current framework documentation; no benchmark claim is made without reproducible evidence.
