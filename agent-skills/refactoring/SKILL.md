---
name: refactoring
description: Restructure code to improve maintainability or design while preserving documented behavior and interfaces.
license: MIT
metadata:
  source: skills/05-code/refactoring.md
  version: "v2"
---

# Refactoring

1. Establish current behavior and the explicit refactoring goal.
2. Inspect tests, interfaces, and affected dependencies.
3. Make a small structural change without changing intended behavior.
4. Run focused tests and repository validation.
5. Review the diff for scope creep and interface changes.
6. Record verification evidence.

## Failure modes
- Scope creep.
- Hidden behavior changes.
- Reduced test coverage.
- Unverified equivalence.

## Evidence
Canonical skill: skills/05-code/refactoring.md
Repository governance: AI_CONSTITUTION.md
