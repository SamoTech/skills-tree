---
title: "Refactoring"
category: 05-code
level: advanced
stability: stable
version: v2
description: "Restructure code to improve maintainability or design while preserving documented behavior and interfaces."
added: "2026-09"
related: [code-review, unit-test-generation, linting-formatting]
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-05-code-refactoring.json)

# Refactoring

**Category:** `code`
**Skill Level:** `advanced`
**Stability:** `stable`
**Added:** 2026-09

### Description

Restructure code to improve maintainability or design while preserving documented behavior and interfaces. The skill is evidence-first: inspect actual state before acting, preserve existing contracts, and verify the result before reporting completion.

### Inputs / Outputs

| Direction | Field | Type | Contract |
|---|---|---|---|
| Input | design_goal | string | The narrow structural goal and the files it may touch |
| Input | tests | object | Coverage that pins current behavior, including characterization tests |
| Output | refactored_code | object | Cleaner structure with behavior and public interfaces preserved |
| Output | evidence | object | Green tests before and after, with a diff bounded to the goal |

### Procedure
1. Confirm tests exist that pin the behavior being preserved; add characterization tests for untested behavior first.
2. Define the design goal narrowly and declare the file scope it may touch.
3. Refactor in small steps, running the tests between steps.
4. Keep public interfaces stable unless the goal explicitly includes an interface change with a migration path.
5. Park unrelated findings as follow-ups; do not mix feature work into the refactoring.
6. Verify equivalence: same tests green, no behavior change, diff reviewed against the stated goal.

### Example

```python
def normalize_name(value: str) -> str:
    return ' '.join(value.split())

assert normalize_name('  example   name ') == 'example name'
print('behavior pinned by assertions before and after restructuring')
```

### Related Skills

- [Code Review](code-review.md) - equivalence review before merge
- [Unit Test Generation](unit-test-generation.md) - pin behavior before restructuring
- [Linting Formatting](linting-formatting.md) - keep style changes separate

## Failure Modes

- Combining refactoring with unrelated feature work.
- Changing public behavior unintentionally.
- Removing or weakening tests instead of preserving coverage.
- Reporting equivalence without verification.

## Changelog
- v2 (2026-11): Structural modernization; added the input/output contract table, a deterministic equivalence example, an execution procedure, and corpus-verified related links.
- v1 (2026-09): Initial entry.

## Evidence

- https://agentskills.io/specification

Evidence status: implementation guidance only; no benchmark claim is made without reproducible evidence.
