---
title: Debugging
category: 05-code
level: advanced
stability: stable
description: Diagnose software defects by isolating symptoms, reproducing failures, identifying root causes, and validating fixes.
added: "2026-09"
related: [05-code]
---

## Description
Diagnose software defects by isolating symptoms, reproducing failures, identifying root causes, and validating fixes. Preserve existing behavior outside the defect and use repository evidence rather than speculation.

## When to Use
Use when a software failure, regression, unexpected result, or reproducible defect must be investigated and corrected.

## Inputs / outputs / failure modes

| Area | Guidance |
|---|---|
| Inputs | Failure symptoms, reproduction steps, source, logs, configuration, and tests. |
| Outputs | Root-cause analysis, minimal fix, and verification evidence. |
| Failure modes | Non-reproducible symptoms, misleading evidence, unrelated changes, or incomplete regression testing. |

## Runnable Example

```python
from pathlib import Path

root = Path('.')
print('repository:', root.resolve())
print('inspect logs, source, and tests before changing code')
```

## Failure modes
- Fixing symptoms without establishing a root cause.
- Changing unrelated code while debugging.
- Ignoring regression coverage.
- Disabling validators to hide a defect.

## Related
- 05-code
- AI_CONSTITUTION.md
- meta/AGENT_OPERATING_MODEL.md

## Evidence
Repository-backed implementation guidance grounded in repository governance and validation workflows; no external benchmark claim is made.
