---
title: Documentation Generation
category: 05-code
level: advanced
stability: stable
description: Generate technical documentation from verified repository behavior, interfaces, configuration, and implementation evidence.
added: "2026-09"
related: [05-code]
---

## Description
Generate technical documentation from verified repository behavior, interfaces, configuration, and implementation evidence. Documentation must describe what the repository actually supports and must not invent APIs or capabilities.

## When to Use
Use when README, API, architecture, configuration, runbook, or developer documentation must be created or refreshed.

## Inputs / outputs / failure modes

| Area | Guidance |
|---|---|
| Inputs | Source, configuration, interfaces, tests, and existing documentation. |
| Outputs | Accurate documentation with traceable repository evidence. |
| Failure modes | Stale claims, invented interfaces, missing prerequisites, or documentation drift. |

## Runnable Example

```python
from pathlib import Path

readme = Path('README.md')
print('README exists:', readme.exists())
print('documentation must follow verified repository behavior')
```

## Failure modes
- Documenting assumptions as facts.
- Omitting prerequisites or operational constraints.
- Updating implementation without updating required documentation.
- Claiming verification that was not performed.

## Related
- 05-code
- AI_CONSTITUTION.md
- meta/AGENT_OPERATING_MODEL.md

## Evidence
Repository-backed implementation guidance grounded in repository governance and validation workflows; no external benchmark claim is made.
