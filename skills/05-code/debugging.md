---
title: "Debugging"
category: 05-code
level: advanced
stability: stable
version: v2
description: "Diagnose software defects by isolating symptoms, reproducing failures, identifying root causes, and validating fixes."
added: "2026-09"
related: [code-search, unit-test-generation, code-review]
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-05-code-debugging.json)

# Debugging

**Category:** `code`
**Skill Level:** `advanced`
**Stability:** `stable`
**Added:** 2026-09

### Description

Diagnose software defects by isolating symptoms, reproducing failures, identifying root causes, and validating fixes. The skill is evidence-first: inspect actual state before acting, preserve existing contracts, and verify the result before reporting completion.

### Inputs / Outputs

| Direction | Field | Type | Contract |
|---|---|---|---|
| Input | symptoms | string | The observed failure, with logs, stack traces, and reproduction steps |
| Input | context | object | Source, configuration, recent changes, and existing tests |
| Output | root_cause | object | The established cause with supporting evidence |
| Output | fix | object | A minimal diff plus a regression test that fails without it |

### Procedure
1. Reproduce the failure deterministically before changing anything; an unreproducible bug can only be guessed at.
2. Bisect the space: logs, stack traces, recent changes, boundary conditions.
3. Form one hypothesis at a time and test it with the smallest possible probe.
4. Establish the root cause with evidence, not plausibility.
5. Implement the minimal fix and add a regression test that fails without it.
6. Re-run the full affected test surface; a single passing case is not fixed.

### Example

```python
def total(prices):
    return sum(prices)

# minimal reproduction of a reported defect
result = total([1, 2, 3])
assert result == 6, f'unexpected total: {result}'
print('repro established; root cause analysis may proceed')
```

### Related Skills

- [Code Search](code-search.md) - locate the failing path and its callers
- [Unit Test Generation](unit-test-generation.md) - pin the fix with a regression test
- [Code Review](code-review.md) - have the fix reviewed before merge

## Failure Modes

- Fixing symptoms without establishing a root cause.
- Changing unrelated code while debugging.
- Disabling validators or tests to hide a defect.
- Reporting fixed without a regression test and full test-surface run.

## Changelog
- v2 (2026-11): Structural modernization; added the input/output contract table, a deterministic reproduction example, an execution procedure, and corpus-verified related links (removed non-corpus repository-file pointers).
- v1 (2026-09): Initial entry.

## Evidence

- https://agentskills.io/specification

Evidence status: implementation guidance only; no benchmark claim is made without reproducible evidence.
