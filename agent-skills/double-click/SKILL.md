---
name: double-click
description: Perform a double-click on a verified UI target using semantic or coordinate-based targeting.
metadata:
  source: skills/10-computer-use/double-click.md
  category: 10-computer-use
  version: "v2"
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-10-computer-use-double-click.json)

# Double Click

**Category:** `computer-use`
**Skill Level:** `advanced`
**Stability:** `stable`
**Added:** 2025-03

### Description

Perform a double-click on a verified UI target using semantic or coordinate-based targeting. The action is contract-first: verify the target and its double-click semantics before acting, and verify the observable postcondition afterwards rather than trusting the acknowledgement.

### Inputs / Outputs

| Direction | Field | Type | Contract |
|---|---|---|---|
| Input | target | object | Verified UI target identity (semantic id preferred, coordinates as fallback) |
| Input | semantics | object | Declared double-click behavior of the target (opens, selects word, zooms) |
| Output | result | object | Performed action acknowledgement with the target used |
| Output | check | object | Verified postcondition (expected dialog/editor state) or explicit failure |

### Procedure
1. Establish the active application and the expected UI state.
2. Verify the target identity before interaction; prefer semantic accessibility identifiers.
3. Confirm the target actually supports double-click semantics and what it triggers.
4. Perform the double-click within the platform's interval threshold and bounds.
5. Re-observe the UI and verify the expected postcondition before continuing.

### Example

```python
action = {
    "capability": "double-click",
    "target": {"strategy": "semantic", "identifier": "invoice-row-3"},
    "semantics": {"opens": "invoice-editor"},
    "interval_ms": 180,
}
assert 40 <= action["interval_ms"] <= 500, "platform double-click interval threshold"
verified = {"target_verified": True, "focus_application": "ledger"}
result = {"performed": action["capability"], "target": action["target"]["identifier"],
          "postcondition_verification_required": "invoice-editor-open"}
print(result)
```

### Related Skills

- [Mouse Click](mouse-click.md) - single-click targeting
- [UI Element Waiting](ui-element-waiting.md) - wait for the target to be interactable
- [Gui Element Anchoring Stability](gui-element-anchoring-stability.md) - stable target anchoring

## Failure Modes

- The click interval exceeds the platform threshold and is interpreted as two single clicks.
- The target moves or re-renders between observation and action.
- The target does not actually support double-click; the fallback single-click dialog opens instead.
- Coordinate drift after a window resize or DPI change clicks the wrong element.
- An intermediate selection state (word selection) is mistaken for the expected postcondition.

## Changelog
- v2 (2026-11): Structural modernization; added the input/output contract table, a deterministic example, an execution procedure, and corpus-verified related links (replaced the non-corpus input-guardrails/output-guardrails/self-category pointers).
- v1 (2025-03): Initial entry.

## Evidence

- https://agentskills.io/specification

Evidence status: implementation guidance only; no benchmark claim is made without reproducible evidence.
