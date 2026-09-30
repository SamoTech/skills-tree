---
name: linting-formatting
description: Apply repository-defined linting and formatting rules consistently while preserving behavior and minimizing unrelated churn.
license: MIT
metadata:
  source: skills/05-code/linting-formatting.md
  version: "v2"
---

# Linting Formatting

1. Inspect repository lint and format configuration and tool versions.
2. Apply the configured tools only to the intended scope.
3. Review the diff for unrelated formatting churn.
4. Run lint and relevant tests.
5. Record verification evidence.

## Failure modes
- Tool version mismatch.
- Unrelated formatting churn.
- Ignored repository configuration.
- Treating lint success as functional proof.

## Evidence
Canonical skill: skills/05-code/linting-formatting.md
Repository governance: AI_CONSTITUTION.md
