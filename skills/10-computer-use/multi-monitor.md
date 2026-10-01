---
title: "Multi Monitor"
category: 10-computer-use
level: advanced
stability: stable
description: "Identify and target a specific display in a multi-monitor environment using verified display geometry and application state."
added: "2025-03"
related: ["10-computer-use", "input-guardrails", "output-guardrails"]
---

**Category:** Computer Use
**Skill Level:** `advanced`
**Stability:** stable

## Description
Identify and target a specific display in a multi-monitor environment using verified display geometry and application state.

## When to Use
Use when an action depends on a particular display or monitor arrangement.

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
action = {"capability": "multi-monitor", "target_verified": True}
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
Display geometry can change dynamically; verify monitor identity and bounds before acting.

## Evidence
Canonical repository skill: this file. Structural conformance is defined by the repository schema, validation workflows, Agent Skills contract, and security gates. Computer-use actions require explicit target verification and postcondition checks.

## Related
- 10-computer-use
- input-guardrails
- output-guardrails
