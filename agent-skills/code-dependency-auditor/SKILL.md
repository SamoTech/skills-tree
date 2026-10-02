---
name: code-dependency-auditor
description: Audit project dependencies for declared usage, version constraints, known risk signals, and unnecessary or inconsistent packages.
metadata:
  source: skills/05-code/dependency-auditor.md
  category: 05-code
---

## Description
Audit project dependencies for declared usage, version constraints, known risk signals, and unnecessary or inconsistent packages. Inspect manifests, lockfiles, build metadata, and repository policy before proposing changes.

## When to Use
Use when dependency inventory, consistency, risk review, or cleanup is explicitly required.

## Inputs / outputs / failure modes

| Area | Guidance |
|---|---|
| Inputs | Manifests, lockfiles, build metadata, repository policy, and package usage. |
| Outputs | Auditable findings and evidence-backed remediation proposals or changes. |
| Failure modes | Missing transitive context, unsafe upgrades, stale metadata, or unsupported risk claims. |

## Runnable Example

```python
from pathlib import Path

names = [p.name for p in Path('.').iterdir() if p.is_file()]
print('top-level files:', len(names))
print('inspect manifests and lockfiles explicitly')
```

## Failure modes
- Treating a package name as proof of runtime usage.
- Ignoring lockfiles or platform constraints.
- Making version changes without compatibility checks.
- Claiming a vulnerability without authoritative evidence.

## Related
- 05-code
- AI_CONSTITUTION.md
- meta/AGENT_OPERATING_MODEL.md

## Evidence
Repository-backed implementation guidance grounded in repository governance and validation workflows; no external benchmark claim is made.
