---
name: linting-formatting
description: Apply repository-defined linting and formatting rules consistently while preserving behavior and minimizing unrelated churn.
metadata:
  source: skills/05-code/linting-formatting.md
  category: 05-code
---

## Description
Apply repository-defined linting and formatting rules consistently while preserving behavior and minimizing unrelated churn. Inspect the configured tools and version before changing source style.

## When to Use
Use when code quality checks require linting, formatting, or normalization.

## Inputs / outputs / failure modes

| Area | Guidance |
|---|---|
| Inputs | Source files, repository configuration, formatter and linter versions. |
| Outputs | Consistently formatted and lint-clean code with verification evidence. |
| Failure modes | Unrelated churn, version mismatch, behavior changes, or ignored configuration. |

## Runnable Example

```python
from pathlib import Path

files = list(Path('.').rglob('*.py'))
print('python files:', len(files))
print('use repository-configured lint and format commands')
```

## Failure modes
- Formatting with an incompatible tool version.
- Mixing style changes with functional changes.
- Ignoring repository configuration.
- Treating lint success as proof of functional correctness.

## Related
- 05-code
- AI_CONSTITUTION.md
- meta/AGENT_OPERATING_MODEL.md

## Evidence
Repository-backed implementation guidance grounded in repository governance and validation workflows; no external benchmark claim is made.
