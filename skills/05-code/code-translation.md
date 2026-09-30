---
title: Code Translation
category: 05-code
level: advanced
stability: stable
description: Translate source code between programming languages while preserving behavior, interfaces, and documented constraints.
added: "2026-09"
related: [05-code]
---

## Description
Translate source code between programming languages while preserving behavior, interfaces, and documented constraints. The procedure is evidence-first: inspect the repository and explicit requirements before changing code, preserve existing contracts, and verify the result with the repository's own tests and quality gates.

## When to Use
Use this skill when the task requires translate source code between programming languages while preserving behavior, interfaces, and documented constraints. Prefer the smallest reversible change that satisfies the stated requirement.

## Inputs / outputs / failure modes

| Area | Guidance |
|---|---|
| Inputs | Repository state, explicit requirements, relevant source/configuration, and existing tests or interfaces. |
| Outputs | A verified implementation or analysis, plus concise evidence of what was checked. |
| Failure modes | Missing requirements, incompatible assumptions, hidden side effects, incomplete verification, or changes that weaken existing controls. |

## Runnable Example

```python
from pathlib import Path

root = Path('.')
files = sorted(p for p in root.rglob('*') if p.is_file())
print(f'Repository files discovered: {len(files)}')
print('Inspect relevant files before making changes.')
```

## Failure modes
- Acting on an inferred requirement instead of an explicit one.
- Modifying unrelated files or interfaces.
- Treating a passing local example as sufficient verification.
- Suppressing or weakening a validator to accommodate an implementation defect.
- Reporting completion without reproducible evidence.

## Related
- [AI Constitution](../../AI_CONSTITUTION.md)
- [Agent operating model](../../meta/AGENT_OPERATING_MODEL.md)

## Evidence
Repository-backed implementation guidance. The skill is grounded in the repository's governance, validation workflows, and evidence-first operating model; no external benchmark claim is made.
