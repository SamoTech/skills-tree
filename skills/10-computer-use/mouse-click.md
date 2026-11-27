---
title: "Mouse Click"
category: 10-computer-use
level: advanced
stability: stable
version: v2
description: "Click a verified UI target using semantic or coordinate-based targeting with postcondition verification."
added: "2025-03"
related: [mouse-move, ui-element-waiting]
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-10-computer-use-mouse-click.json)

# Mouse Click

**Category:** `computer-use`
**Skill Level:** `advanced`
**Stability:** `stable`
**Added:** 2025-03

### Description

Click a verified UI target using semantic or coordinate-based targeting with postcondition verification. The action is contract-first: verify the target and UI state before clicking, act within the declared bounds, and verify the observable postcondition afterwards rather than trusting the acknowledgement.

### Inputs / Outputs

| Direction | Field | Type | Contract |
|---|---|---|---|
| Input | target | object | Verified UI target identity (semantic id preferred, coordinates as fallback) |
| Input | bounds | object | Declared click scope (single click, no drag, no chained actions) |
| Output | result | object | Performed action acknowledgement with the target used |
| Output | check | object | Verified postcondition (expected UI state) or explicit failure |

### Procedure
1. Establish the active application, target, and expected UI state.
2. Verify the target before interaction; prefer semantic accessibility identifiers when available.
3. Perform only the requested click within the declared bounds.
4. Inspect the resulting UI state and verify the expected postcondition.
5. Stop and report ambiguity rather than guessing when the UI differs from the expected state.

### Example

```python
action = {"capability": "mouse-click",
          "target": {"strategy": "semantic", "identifier": "submit-order-button"},
          "bounds": {"single_click": True, "no_drag": True}}
assert action["bounds"]["single_click"] and not action["bounds"]["no_drag"]
verified = {"target_verified": True, "focus_application": "checkout"}
assert verified["target_verified"]
result = {"status": "postcondition_required", "capability": action["capability"],
          "target": action["target"]["identifier"]}
print(result)
```

### Related Skills

- [Mouse Move](mouse-move.md) - pointer positioning before a click
- [UI Element Waiting](ui-element-waiting.md) - wait for interactability
- [Approval Before Destructive Tools](../14-security/approval-before-destructive-tools.md) - gate destructive clicks

## Failure Modes

- Target or application identity cannot be verified.
- UI changed between observation and action (stale UI, overlay intercepts the click).
- Focus is ambiguous or lost.
- Click may have destructive or irreversible side effects without an approval gate.
- Postcondition cannot be verified.

## Changelog
- v2 (2026-11): Structural modernization; added the input/output contract table, a deterministic example, an execution procedure, and corpus-verified related links (replaced the non-corpus input-guardrails/output-guardrails/self-category pointers).
- v1 (2025-03): Initial entry.

## Evidence

- https://agentskills.io/specification

Evidence status: implementation guidance only; no benchmark claim is made without reproducible evidence.
