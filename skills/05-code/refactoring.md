---
title: Refactoring
category: 05-code
level: advanced
stability: stable
description: Restructure code to improve maintainability or design while preserving documented behavior and interfaces.
added: "2026-09"
related: [05-code]
---

## Description
Restructure code to improve maintainability or design while preserving documented behavior and interfaces. Refactoring is evidence-driven: establish current behavior, make a bounded change, and verify equivalence.

## When to Use
Use when structure, duplication, coupling, readability, or maintainability needs improvement without changing intended behavior.

## Inputs / outputs / failure modes

| Area | Guidance |
|---|---|
| Inputs | Current implementation, tests, interfaces, and explicit design goal. |
| Outputs | Cleaner structure with preserved behavior and verification evidence. |
| Failure modes | Scope creep, hidden behavior changes, incomplete coverage, or API breakage. |

## Runnable Example

```python
def normalize_name(value: str) -> str:
    return ' '.join(value.split())

print(normalize_name('  example   name '))
print('refactor only after behavior is understood')
```

## Failure modes
- Combining refactoring with unrelated feature work.
- Changing public behavior unintentionally.
- Removing tests instead of preserving coverage.
- Reporting equivalence without verification.

## Related
- 05-code
- AI_CONSTITUTION.md
- meta/AGENT_OPERATING_MODEL.md

## Evidence
Repository-backed implementation guidance grounded in repository governance and validation workflows; no external benchmark claim is made.
