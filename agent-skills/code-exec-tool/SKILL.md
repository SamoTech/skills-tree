---
name: code-exec-tool
description: Execute code in an explicitly scoped runtime while validating inputs, outputs, resource limits, and side effects.
license: MIT
metadata:
  source: skills/07-tool-use/code-exec-tool.md
  version: "v2"
---

# Code Exec Tool

1. Inspect the documented interface and repository contract.
2. Validate inputs and authorization boundaries.
3. Invoke only the intended operation.
4. Validate the response and resulting state.
5. Record verification evidence.

## Failure modes
- Undocumented interface usage.
- Invalid inputs or excessive permissions.
- Unverified outcomes.

## Evidence
Canonical skill: skills/07-tool-use/code-exec-tool.md
Repository governance: AI_CONSTITUTION.md
