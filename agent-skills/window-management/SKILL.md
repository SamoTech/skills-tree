---
name: window-management
description: Move, resize, minimize, maximize, or focus a verified application window within explicit bounds.
metadata:
  source: skills/10-computer-use/window-management.md
  category: 10-computer-use
---

**Category:** Computer Use
**Skill Level:** `advanced`
**Stability:** stable

## Description
Move, resize, minimize, maximize, or focus a verified application window within explicit bounds.

## When to Use
Use when window state must be changed for a subsequent task.

## Inputs / Outputs / Failure Modes
| Area | Contract |
|---|---|
| Inputs | Verified UI/session state, target identity, action parameters, authorization, and expected postcondition. |
| Outputs | Bounded computer-use action plus verified resulting state or an explicit failure. |
| Failure modes | Stale UI, wrong target, geometry drift, permission failure, or unexpected side effects. |

## Procedure
1. Establish the active application/session and expected UI state.
2. Verify target identity and bounds before interaction.
3. Perform only the requested bounded action.
4. Re-observe the resulting UI and verify the expected postcondition.
5. Stop when the observed state differs materially from the expected state.

## Runnable Example
```python
action = {"capability": "window-management", "target_verified": True}
assert action["target_verified"]
result = {"status": "postcondition_required", "capability": action["capability"]}
print(result)
```

## Failure Modes
- Target or session identity cannot be verified.
- UI or display geometry changed after observation.
- Action may expose sensitive data or cause destructive effects.
- Focus or permission is ambiguous.
- Postcondition cannot be verified.

## Safety Boundary
Window handles and geometry can become stale; verify identity and resulting bounds after each change.

## Evidence
Canonical repository skill: this file. Structural conformance is defined by the repository schema, validation workflows, Agent Skills contract, and security gates. Computer-use actions require explicit target verification and postcondition checks.

## Related
- 10-computer-use
- input-guardrails
- output-guardrails
