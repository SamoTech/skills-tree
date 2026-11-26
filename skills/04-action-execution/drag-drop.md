---
title: "Drag and Drop"
category: 04-action-execution
level: intermediate
stability: stable
version: v2
description: "Perform a bounded desktop or browser drag-and-drop action using verified source and destination targets, then confirm the resulting state."
added: "2026-09"
related: [mouse-input, screenshot-capture, assertion]
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-04-action-execution-drag-drop.json)

# Drag and Drop

**Category:** `action-execution`
**Skill Level:** `intermediate`
**Stability:** `stable`
**Added:** 2026-09

### Description

Move an interface object from a verified source location to a verified destination, then confirm the resulting state. Coordinate-only gestures are sensitive to layout changes, so prefer element locators over raw coordinates and always verify the postcondition instead of assuming the gesture succeeded.

### Inputs / Outputs

| Direction | Field | Type | Contract |
|---|---|---|---|
| Input | `source` | locator or coordinates | The element to drag; resolved and visible before the gesture |
| Input | `destination` | locator or coordinates | The drop target; resolved and visible before the gesture |
| Input | `postcondition` | predicate | A checkable property that must hold after the drop |
| Output | `drop_result` | `{dropped, verified}` | Whether the gesture ran and the postcondition held |
| Output | `failure` | string or `None` | The specific failure when the drop is not verified |

### Procedure
1. Resolve the source and destination locators and assert both are visible and enabled before dragging.
2. Prefer element-to-element drag APIs over absolute coordinates; if coordinates are unavoidable, re-resolve them immediately before the gesture.
3. Check that the destination is not a destructive target (delete zone, external site) without explicit authorization.
4. Perform the drag, then evaluate the postcondition against the actual interface state.
5. Treat a satisfied postcondition as the only success signal; a completed gesture without a verified state is a failure.
6. On failure, restore or report the pre-drag state rather than retrying blindly.

### Example

```python
def verified_drag(page, source_sel: str, target_sel: str, expect_attr: tuple[str, str]) -> dict:
    source = page.locator(source_sel)
    target = page.locator(target_sel)
    source.wait_for(state="visible")
    target.wait_for(state="visible")
    source.drag_to(target)
    attr, expected = expect_attr
    actual = target.get_attribute(attr)
    return {"dropped": True, "verified": actual == expected, "failure": None if actual == expected else f"{attr}={actual}"}

result = verified_drag(
    page, "[data-testid='source']", "[data-testid='target']",
    expect_attr=("data-state", "received"),
)
print(result)
```

### Related Skills

- [Mouse Input](mouse-input.md)
- [Screenshot Capture](screenshot-capture.md)
- [Assertion](assertion.md)

## Failure Modes

- Dragging by stale coordinates after a layout change: re-resolve locators immediately before the gesture.
- Dropping into a destructive target without an explicit authorization boundary.
- Treating a completed gesture as success: only a checked postcondition counts.
- Native (OS-level) drag targets not reacting to synthetic HTML5/pointer events: verify the drop with the actual application state and report the incompatibility instead of forcing retries.
- Untrusted or user-supplied locators executed without validation.

## Changelog
- v2 (2026-11): Structural modernization; added the input/output contract table, an explicit procedure, a deterministic verification example, expanded failure modes, and version history.
- v1 (2026-09): Initial entry.

## Evidence

- https://agentskills.io/specification

Evidence status: implementation guidance only; no benchmark claim is made without reproducible evidence.
