---
name: unit-test-generation
description: Generate focused unit tests that verify isolated behavior, edge cases, and failure handling from explicit contracts.
metadata:
  source: skills/05-code/unit-test-generation.md
  category: 05-code
---

## Description
Generate focused unit tests that verify isolated behavior, edge cases, and failure handling from explicit contracts. Tests should be deterministic, readable, and aligned with repository conventions.

## When to Use
Use when a unit-level behavior needs regression coverage or when implementation changes require focused tests.

## Inputs / outputs / failure modes

| Area | Guidance |
|---|---|
| Inputs | Function or component contract, dependencies, expected behavior, and edge cases. |
| Outputs | Deterministic unit tests with meaningful assertions. |
| Failure modes | Weak assertions, excessive mocking, missing boundaries, or flaky setup. |

## Runnable Example

```python
def add(a: int, b: int) -> int:
    return a + b

assert add(2, 3) == 5
assert add(0, 0) == 0
```

## Failure modes
- Testing implementation details instead of behavior.
- Missing boundary and failure cases.
- Over-mocking dependencies needed to establish behavior.
- Tests that pass without meaningful assertions.

## Related
- 05-code
- AI_CONSTITUTION.md
- meta/AGENT_OPERATING_MODEL.md

## Evidence
Repository-backed implementation guidance grounded in repository governance and validation workflows; no external benchmark claim is made.
