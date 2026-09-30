---
name: a2a-tool
description: Use agent-to-agent tool interfaces with explicit contracts, authorization boundaries, message validation, and observable outcomes.
license: MIT
metadata:
  source: skills/07-tool-use/a2a-tool.md
  version: "v2"
---

# A2a Tool

1. Identify the documented tool contract and authorization boundary.
2. Validate the request shape and required inputs.
3. Invoke only the intended interface.
4. Validate the response and resulting state.
5. Record evidence of the completed operation.

## Failure modes
- Undocumented interface usage.
- Invalid or excessive request data.
- Unverified outcomes.
- Authorization boundary violations.

## Evidence
Canonical skill: skills/07-tool-use/a2a-tool.md
Repository governance: AI_CONSTITUTION.md
