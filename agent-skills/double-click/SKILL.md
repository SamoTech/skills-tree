---
name: double-click
description: Perform a double-click on a verified UI target using semantic or coordinate-based targeting.
metadata:
  source: skills/10-computer-use/double-click.md
  category: 10-computer-use
---

**Category:** Computer Use
**Skill Level:** `advanced`
**Stability:** stable

## Description
Perform a double-click on a verified UI target using semantic or coordinate-based targeting.

## When to Use
Use when the target and intended double-click action are unambiguous.

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
action = {"capability": "double-click", "target_verified": True}
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
Re-check target identity and postcondition; double-click can trigger destructive or irreversible UI actions.

## Evidence
Canonical repository skill: this file. Structural conformance is defined by the repository schema, validation workflows, Agent Skills contract, and security gates. Computer-use actions require target verification and postcondition checks.

## Related
- 10-computer-use
- input-guardrails
- output-guardrails
