---
name: dependency-management
description: Manage software dependencies through explicit version constraints, reproducible updates, compatibility checks, and rollback-safe changes.
license: MIT
metadata:
  source: skills/05-code/dependency-management.md
  version: "v2"
---

# Dependency Management

1. Inspect manifests, lockfiles, runtime constraints, and repository policy.
2. Define the exact dependency change and compatibility boundary.
3. Update manifests and lockfiles reproducibly.
4. Run relevant build, dependency, and regression validation.
5. Check the diff for unintended transitive or platform changes.
6. Record verification and recovery evidence.

## Failure modes
- Unbounded or incompatible upgrades.
- Manifest and lockfile drift.
- Missing regression validation.
- No recovery path for high-impact changes.

## Evidence
Canonical skill: skills/05-code/dependency-management.md
Repository governance: AI_CONSTITUTION.md
