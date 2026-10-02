---
name: bug-fixing
description: Fix a reproducible defect by isolating the failing behavior, making the smallest safe change, and verifying regression coverage.
metadata:
  source: skills/05-code/bug-fixing.md
  category: 05-code
---

# Bug Fixing

## Description

Fix a reproducible defect by isolating the failing behavior, making the smallest safe change, and verifying regression coverage.

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
def fixed_total(values):
    if values is None: return 0
    return sum(values)

assert fixed_total([1, 2, 3]) == 6
assert fixed_total(None) == 0
print('regression verified')
```

## Failure modes

- Implementing behavior not supported by the requirements.
- Changing unrelated code.
- Skipping regression or security verification.
- Claiming correctness without evidence.

## Related

- `debugging.md`
- `unit-test-generation.md`
- `git-diff-reading.md`

## Evidence

- AI_CONSTITUTION.md
- AGENTS.md
- Repository validation and security workflows

Evidence status: repository-backed implementation guidance; no benchmark claim.
