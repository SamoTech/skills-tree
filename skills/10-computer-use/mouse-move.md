---
title: "Mouse Move"
category: 10-computer-use
level: advanced
stability: stable
version: v2
description: "Move the pointer to a verified UI target using semantic or coordinate-based targeting."
added: "2025-03"
related: [mouse-click, gui-element-anchoring-stability]
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-10-computer-use-mouse-move.json)

# Mouse Move

**Category:** `computer-use`
**Skill Level:** `advanced`
**Stability:** `stable`
**Added:** 2025-03

### Description

Move the pointer to a verified UI target using semantic or coordinate-based targeting. Pointer movement alone can trigger hover states, tooltips, and menus; the move is contract-first: verify the target, move within bounds, and confirm the resting state before any subsequent action.

### Inputs / Outputs

| Direction | Field | Type | Contract |
|---|---|---|---|
| Input | target | object | Verified target point or element identity in the correct coordinate space |
| Input | hover | object | Declared hover tolerance (whether tooltips/menus triggered by the move are acceptable) |
| Output | position | object | Resting pointer coordinates and the element under the pointer |
| Output | check | object | Verified hover state or explicit mismatch failure |

### Procedure
1. Establish the active application/session and the expected UI state.
2. Resolve the target into the session's actual coordinate space (DPI scaling, remote-session mapping).
3. Move the pointer to the verified target; allow hover state to settle if tooltips are declared acceptable.
4. Verify the element under the pointer matches the intended target.
5. Stop and report when the hover state or pointer target differs from the expected state.

### Example

```python
move = {"capability": "mouse-move",
        "target": {"strategy": "semantic", "identifier": "help-icon"},
        "hover": {"tooltips_acceptable": True, "settle_ms": 400}}
coords = {"x": 1180, "y": 42, "space": "session-dpi-2x"}
assert coords["space"] == "session-dpi-2x", "coordinate space must match the session"
under_pointer = {"element": "help-icon"}
assert under_pointer["element"] == move["target"]["identifier"], "pointer rests on wrong element"
print({"moved": True, "resting": under_pointer["element"], "hover_settled": True})
```

### Related Skills

- [Mouse Click](mouse-click.md) - the click that usually follows
- [Gui Element Anchoring Stability](gui-element-anchoring-stability.md) - stable anchors under re-render
- [Multi Monitor](multi-monitor.md) - targeting across displays

## Failure Modes

- The move crosses an element with hover behavior, opening a tooltip or menu that shifts the UI.
- DPI or remote-session scaling maps the coordinates to the wrong physical point.
- A target animation or layout shift moves the element after the move completes.
- The pointer rests on a different element than the one verified (overlay intercept).
- Hover state never settles because the UI keeps animating.

## Changelog
- v2 (2026-11): Structural modernization; added the input/output contract table, a deterministic example, an execution procedure, and corpus-verified related links (replaced the non-corpus input-guardrails/output-guardrails/self-category pointers).
- v1 (2025-03): Initial entry.

## Evidence

- https://agentskills.io/specification

Evidence status: implementation guidance only; no benchmark claim is made without reproducible evidence.
