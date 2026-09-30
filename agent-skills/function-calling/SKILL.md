---
name: function-calling
description: Invoke typed functions using explicit schemas, validated arguments, bounded side effects, and verified results.
license: MIT
metadata:
  source: skills/07-tool-use/function-calling.md
  version: "v2"
---

# Function Calling

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
Canonical skill: skills/07-tool-use/function-calling.md
Repository governance: AI_CONSTITUTION.md
