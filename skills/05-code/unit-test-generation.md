---
title: "Unit Test Generation"
category: 05-code
level: advanced
stability: stable
version: v2
description: "Generate focused unit tests that verify isolated behavior, edge cases, and failure handling from explicit contracts."
added: "2026-09"
related: [integration-test-writing, code-review, refactoring]
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-05-code-unit-test-generation.json)

# Unit Test Generation

**Category:** `code`
**Skill Level:** `advanced`
**Stability:** `stable`
**Added:** 2026-09

### Description

Generate focused unit tests that verify isolated behavior, edge cases, and failure handling from explicit contracts. The skill is evidence-first: inspect actual state before acting, preserve existing contracts, and verify the result before reporting completion.

### Inputs / Outputs

| Direction | Field | Type | Contract |
|---|---|---|---|
| Input | contract | object | The function or component behavior, boundaries, and error paths to cover |
| Output | tests | list | Deterministic tests, one behavior each, with meaningful assertions |
| Output | coverage_notes | object | Cases included and explicitly excluded, with reasons |

### Procedure
1. Derive cases from the contract: normal paths, boundaries, and error paths, not from implementation internals.
2. Write one behavior per test with a name that states the expectation.
3. Assert on observable outcomes; avoid asserting call internals.
4. Keep tests deterministic: fixed inputs, no uncontrolled network, time, or randomness.
5. Mock only boundaries the unit does not own; over-mocking hides real defects.
6. Verify the tests fail on a deliberately broken implementation before trusting them.

### Example

```python
def add(a: int, b: int) -> int:
    return a + b

assert add(2, 3) == 5
assert add(0, 0) == 0
assert add(-1, 1) == 0
print('contract cases: normal, zero, and boundary covered')
```

### Related Skills

- [Integration Test Writing](integration-test-writing.md) - boundary coverage beyond units
- [Code Review](code-review.md) - review assertion quality, not just presence
- [Refactoring](refactoring.md) - pin behavior before restructuring

## Failure Modes

- Testing implementation details instead of behavior.
- Missing boundary and failure cases.
- Over-mocking dependencies needed to establish behavior.
- Tests that pass without meaningful assertions.

## Changelog
- v2 (2026-11): Structural modernization; added the input/output contract table, a deterministic multi-case example, an execution procedure, and corpus-verified related links.
- v1 (2026-09): Initial entry.

## Evidence

- https://agentskills.io/specification

Evidence status: implementation guidance only; no benchmark claim is made without reproducible evidence.
