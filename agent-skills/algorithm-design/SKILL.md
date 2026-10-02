---
name: algorithm-design
description: Design an algorithm from explicit requirements, constraints, invariants, complexity targets, and testable acceptance criteria.
metadata:
  source: skills/05-code/algorithm-design.md
  category: 05-code
---

# Algorithm Design

## Description

Design an algorithm from explicit requirements, constraints, invariants, complexity targets, and testable acceptance criteria.

## When to Use

- Use when the code task has explicit acceptance criteria.
- Preserve repository conventions and existing security gates.
- Verify behavior before reporting completion.

## Inputs / outputs / failure modes

| Input | Output | Failure mode |
|---|---|---|
| Requirements | Code or analysis | Ambiguous requirement |
| Repository context | Compatible change | Convention mismatch |
| Tests/evidence | Verification result | Regression |
| Security constraints | Safe implementation | Gate bypass |

## Runnable Example

```python
def algorithm(values):
    values = list(values)
    return sorted(values)

assert algorithm([3, 1, 2]) == [1, 2, 3]
print('algorithm contract verified')
```

## Failure modes

- Implementing behavior not supported by the requirements.
- Changing unrelated code.
- Skipping regression or security verification.
- Claiming correctness without evidence.

## Related

- `defining-requirements.md`
- `testing.md`

## Evidence

- AI_CONSTITUTION.md
- AGENTS.md
- Repository validation and security workflows

Evidence status: repository-backed implementation guidance; no benchmark claim.
