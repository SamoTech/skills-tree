---
name: debugging
description: Diagnose software defects by isolating symptoms, reproducing failures, identifying root causes, and validating fixes.
license: MIT
metadata:
  source: skills/05-code/debugging.md
  version: "v2"
---

# Debugging

1. Load the repository state and the exact failure report.
2. Reproduce the defect using the smallest reliable case.
3. Inspect relevant source, configuration, logs, and tests.
4. Identify and document the root cause before changing code.
5. Implement the smallest compatible fix and add regression coverage when appropriate.
6. Run relevant validation and record evidence.

## Failure modes
- Treating symptoms as root cause.
- Making unrelated changes.
- Skipping regression verification.
- Weakening validators or security controls.

## Evidence
Canonical skill: skills/05-code/debugging.md
Repository governance: AI_CONSTITUTION.md
