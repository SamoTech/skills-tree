---
name: dependency-management
description: Manage software dependencies through explicit version constraints, reproducible updates, compatibility checks, and rollback-safe changes.
metadata:
  source: skills/05-code/dependency-management.md
  category: 05-code
  version: "v2"
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-05-code-dependency-management.json)

# Dependency Management

**Category:** `code`
**Skill Level:** `advanced`
**Stability:** `stable`
**Added:** 2026-09

### Description

Manage software dependencies through explicit version constraints, reproducible updates, compatibility checks, and rollback-safe changes. The skill is evidence-first: inspect actual state before acting, preserve existing contracts, and verify the result before reporting completion.

### Inputs / Outputs

| Direction | Field | Type | Contract |
|---|---|---|---|
| Input | change | object | The dependency intent: add, remove, upgrade, downgrade, or pin |
| Input | constraints | object | Runtime versions, platform support, and license policy |
| Output | dependency_state | object | Manifest and lockfile updated together and consistent |
| Output | rollback | object | The previous pinned state, recorded before the change |

### Procedure
1. Record the current pinned state so the change is reversible.
2. Change the manifest and lockfile together; never commit one without the other.
3. Respect runtime and platform constraints; prefer bounded ranges plus a lockfile over floating versions.
4. Install in a clean environment and run the affected test suites.
5. Document transitive consequences and any required code adjustments.
6. If verification fails, roll back to the recorded state rather than layering workarounds.

### Example

```python
pinned = {'pydantic': '2.9.0', 'httpx': '0.27.0'}
lockfile = {'pydantic': '2.9.0', 'httpx': '0.27.0'}
assert pinned == lockfile, 'manifest and lockfile must agree'
print('dependency state consistent and recorded for rollback')
```

### Related Skills

- [Dependency Auditor](dependency-auditor.md) - audit before and after changes
- [Git Operations](git-operations.md) - commit manifest and lockfile together
- [Debugging](debugging.md) - diagnose update-induced regressions

## Failure Modes

- Updating without respecting runtime constraints.
- Committing inconsistent manifests and lockfiles.
- Skipping compatibility and regression tests.
- Making irreversible changes without recovery evidence.

## Changelog
- v2 (2026-11): Structural modernization; added the input/output contract table, a deterministic consistency example, an execution procedure, and corpus-verified related links.
- v1 (2026-09): Initial entry.

## Evidence

- https://agentskills.io/specification

Evidence status: implementation guidance only; no benchmark claim is made without reproducible evidence.
