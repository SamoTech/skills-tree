---
name: dependency-management
description: Manage software dependencies through explicit version constraints, reproducible updates, compatibility checks, and rollback-safe changes.
metadata:
  source: skills/05-code/dependency-management.md
  category: 05-code
---

## Description
Manage software dependencies through explicit version constraints, reproducible updates, compatibility checks, and rollback-safe changes. Preserve lockfile integrity and verify application behavior after updates.

## When to Use
Use for dependency additions, removals, upgrades, downgrades, lockfile refreshes, and compatibility remediation.

## Inputs / outputs / failure modes

| Area | Guidance |
|---|---|
| Inputs | Manifest, lockfile, runtime constraints, compatibility requirements, and tests. |
| Outputs | Reproducible dependency state with verification evidence. |
| Failure modes | Unbounded upgrades, lockfile drift, incompatible transitive changes, or missing rollback. |

## Runnable Example

```python
from pathlib import Path

for name in ('package.json', 'pyproject.toml', 'requirements.txt'):
    p = Path(name)
    print(name, 'present=' + str(p.exists()))
```

## Failure modes
- Updating without respecting runtime constraints.
- Committing inconsistent manifests and lockfiles.
- Skipping compatibility and regression tests.
- Making irreversible changes without recovery evidence.

## Related
- 05-code
- AI_CONSTITUTION.md
- meta/AGENT_OPERATING_MODEL.md

## Evidence
Repository-backed implementation guidance grounded in repository governance and validation workflows; no external benchmark claim is made.
