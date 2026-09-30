---
name: dependency-auditor
description: Audit project dependencies for declared usage, version constraints, known risk signals, and unnecessary or inconsistent packages.
license: MIT
metadata:
  source: skills/05-code/dependency-auditor.md
  version: "v2"
---

# Dependency Auditor

1. Inspect manifests, lockfiles, build metadata, and repository dependency policy.
2. Determine declared, transitive, and referenced dependencies.
3. Compare versions and constraints against explicit compatibility requirements.
4. Identify unnecessary, inconsistent, or risk-relevant dependencies using authoritative evidence.
5. Propose or implement the smallest safe remediation.
6. Run dependency and repository validation and record evidence.

## Failure modes
- Unsupported risk or usage claims.
- Ignoring lockfiles or platform constraints.
- Unsafe dependency upgrades.
- Incomplete verification.

## Evidence
Canonical skill: skills/05-code/dependency-auditor.md
Repository governance: AI_CONSTITUTION.md
