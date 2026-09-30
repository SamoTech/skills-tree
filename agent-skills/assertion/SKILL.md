---
name: assertion
description: Check an explicit execution invariant and stop safely when the expected state is not true.
license: MIT
metadata:
  source: skills/04-action-execution/assertion.md
  version: "v2"
---

# Assertion

1. Define the condition that must hold before continuing.
2. Evaluate it against current verified state.
3. Fail closed with an actionable message when false.
4. Preserve evidence needed to diagnose the failed invariant.

## Failure modes

- Continuing after a failed assertion.
- Checking stale state.
- Using an assertion as a substitute for authorization.

## Evidence

- skills/04-action-execution/assertion.md
- AI_CONSTITUTION.md
- AGENTS.md

Evidence status: repository operating guidance; no benchmark claim.
