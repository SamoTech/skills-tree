---
name: dockerfile-generation
description: Generate maintainable Dockerfiles from application runtime requirements, build inputs, security constraints, and deployment targets.
metadata:
  source: skills/05-code/dockerfile-generation.md
  category: 05-code
---

## Description
Generate maintainable Dockerfiles from verified application runtime requirements, build inputs, security constraints, and deployment targets. Inspect the repository before making assumptions and verify the resulting image behavior.

## When to Use
Use when container packaging or a Dockerfile change is explicitly required.

## Inputs / outputs / failure modes

| Area | Guidance |
|---|---|
| Inputs | Runtime, build system, dependencies, configuration, and deployment constraints. |
| Outputs | A reproducible container build definition with verification evidence. |
| Failure modes | Missing runtime assets, incorrect startup behavior, non-reproducible builds, or incomplete verification. |

## Runnable Example

```python
from pathlib import Path
files = [p.name for p in Path('.').iterdir() if p.is_file()]
print('files:', files[:10])
print('inspect runtime metadata before generating a Dockerfile')
```

## Failure modes
- Guessing runtime dependencies.
- Omitting required build artifacts.
- Skipping an image build or startup check.
- Changing unrelated deployment behavior.

## Related
- 05-code
- AI_CONSTITUTION.md
- meta/AGENT_OPERATING_MODEL.md

## Evidence
Repository-backed implementation guidance grounded in repository governance and validation workflows; no external benchmark claim is made.
