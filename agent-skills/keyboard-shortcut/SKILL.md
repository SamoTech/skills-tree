---
name: keyboard-shortcut
description: Execute a specified keyboard shortcut against the verified active application and UI context.
metadata:
  source: skills/10-computer-use/keyboard-shortcut.md
  category: 10-computer-use
---

**Category:** Computer Use
**Skill Level:** `advanced`
**Stability:** stable

## Description
Execute a specified keyboard shortcut against the verified active application and UI context.

## When to Use
Use when the shortcut is known and the focused target is verified.

## Inputs / Outputs / Failure Modes
| Area | Contract |
|---|---|
| Inputs | Verified UI state, target identity, action parameters, authorization, and expected postcondition. |
| Outputs | Performed action plus verified resulting UI state or an explicit failure. |
| Failure modes | Stale UI, wrong focus/target, coordinate drift, permission failure, or unexpected side effects. |

## Procedure
1. Establish the active application, target, and expected UI state.
2. Verify the target before interaction; prefer semantic accessibility identifiers when available.
3. Perform only the requested action within the declared bounds.
4. Inspect the resulting UI state and verify the expected postcondition.
5. Stop and report ambiguity rather than guessing when the UI differs from the expected state.

## Runnable Example
```python
action = {"capability": "keyboard-shortcut", "target_verified": True}
assert action["target_verified"]
result = {"status": "postcondition_required", "capability": action["capability"]}
print(result)
```

## Failure Modes
- Target or application identity cannot be verified.
- UI changed between observation and action.
- Focus is ambiguous or lost.
- Action may have destructive or irreversible side effects.
- Postcondition cannot be verified.

## Safety Boundary
Shortcuts are context-sensitive and may trigger destructive actions; verify focus and postcondition.

## Evidence
Canonical repository skill: this file. Structural conformance is defined by the repository schema, validation workflows, Agent Skills contract, and security gates. Computer-use actions require target verification and postcondition checks.

## Related
- 10-computer-use
- input-guardrails
- output-guardrails
