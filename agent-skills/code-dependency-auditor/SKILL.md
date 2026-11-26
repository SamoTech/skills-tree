---
name: code-dependency-auditor
description: Audit project dependencies for declared usage, version constraints, known risk signals, and unnecessary or inconsistent packages.
metadata:
  source: skills/05-code/dependency-auditor.md
  category: 05-code
  version: "v2"
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-05-code-dependency-auditor.json)

# Dependency Auditor (Project Manifests)

**Category:** `code`
**Skill Level:** `advanced`
**Stability:** `stable`
**Added:** 2026-09

### Description

Audit project dependencies for declared usage, version constraints, known risk signals, and unnecessary or inconsistent packages. The skill is evidence-first: inspect actual state before acting, preserve existing contracts, and verify the result before reporting completion.

### Inputs / Outputs

| Direction | Field | Type | Contract |
|---|---|---|---|
| Input | manifests | list of string | Manifests, lockfiles, and build metadata paths |
| Input | policy | object | Allowed licenses, version constraints, and pinning rules |
| Output | inventory | object | Declared packages versus actually imported packages |
| Output | findings | list of object | Unused, inconsistent, stale, or risky entries, each with evidence |

### Procedure
1. Enumerate declared dependencies from manifests and lockfiles.
2. Cross-check declared names against actual imports and calls; unused declarations are findings.
3. Check version-constraint consistency between manifest and lockfile.
4. Screen for risk signals (advisories from authoritative sources, abandoned packages, unusual install scripts) and cite the source for every claim.
5. Propose remediations that respect runtime constraints and the pinning policy.
6. Never claim a vulnerability without an authoritative reference.

### Example

```python
declared = {'requests': '2.31.0', 'unused-lib': '1.0.0'}
imported = {'requests'}
unused = sorted(set(declared) - imported)
assert unused == ['unused-lib']
print('audit findings:', unused)
```

### Related Skills

- [
- D
- e
- p
- e
- n
- d
- e
- n
- c
- y
-
- M
- a
- n
- a
- g
- e
- m
- e
- n
- t
- ]
- (
- d
- e
- p
- e
- n
- d
- e
- n
- c
- y
- -
- m
- a
- n
- a
- g
- e
- m
- e
- n
- t
- .
- m
- d
- )
-
- -
-
- a
- p
- p
- l
- y
-
- r
- e
- m
- e
- d
- i
- a
- t
- i
- o
- n
- s
-
- r
- e
- v
- e
- r
- s
- i
- b
- l
- y
- ,
- [
- C
- o
- d
- e
-
- R
- e
- v
- i
- e
- w
- ]
- (
- c
- o
- d
- e
- -
- r
- e
- v
- i
- e
- w
- .
- m
- d
- )
-
- -
-
- a
- u
- d
- i
- t
-
- f
- i
- n
- d
- i
- n
- g
- s
-
- r
- e
- v
- i
- e
- w
- e
- d
-
- b
- e
- f
- o
- r
- e
-
- c
- h
- a
- n
- g
- e
- s
-
- m
- e
- r
- g
- e

## Failure Modes

- Treating a declared package name as proof of runtime usage.
- Ignoring lockfiles or platform markers.
- Recommending version changes without compatibility checks.
- Claiming a vulnerability without an authoritative source.

## Changelog
- v2 (2026-11): Structural modernization; added the input/output contract table, a deterministic audit example, an execution procedure, and corpus-verified related links.
- v1 (2026-11): Title disambiguated per DECISION-2026-11-26-TITLE-UNIQUENESS; capability contract unchanged.
- v1 (2026-09): Initial entry.

## Evidence

- https://agentskills.io/specification

Evidence status: implementation guidance only; no benchmark claim is made without reproducible evidence.
