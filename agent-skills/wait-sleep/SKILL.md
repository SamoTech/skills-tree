---
name: wait-sleep
description: Pause for a bounded duration or polling interval without treating elapsed time as proof of state.
license: MIT
metadata:
  source: skills/04-action-execution/wait-sleep.md
  version: "v2"
---

# wait-sleep

1. Verify the target, scope, and authorization before acting.
2. Apply explicit bounds for input, duration, resources, and external effects.
3. Execute only the requested operation.
4. Verify the resulting state when the action has consequential effects.

## Failure modes

- Acting on an ambiguous or stale target.
- Exceeding configured resource or time bounds.
- Leaking sensitive input or environment data.
- Reporting success without postcondition evidence.

## Evidence

- skills/04-action-execution/wait-sleep.md
- AI_CONSTITUTION.md
- AGENTS.md

Evidence status: repository-backed implementation guidance; no benchmark claim.
