---
title: "Drag and Drop"
category: 04-action-execution
level: intermediate
stability: stable
description: "Perform a bounded desktop or browser drag-and-drop action using verified source and destination targets."
added: "2026-09"
related: [mouse-input, screenshot-capture, assertion]
---

# Drag and Drop

## Description

Move an interface object from a verified source location to a verified destination. Confirm the resulting state because coordinate-only actions are sensitive to layout changes.

## When to Use

- Browser workflows with draggable elements.
- Desktop applications with drag-and-drop controls.
- Moving an explicitly identified item between targets.

## Inputs / outputs / failure modes

| Input | Output | Failure mode |
|---|---|---|
| Source locator | Drag gesture | Source not found |
| Destination locator | Drop result | Wrong target |
| Coordinate fallback | Mouse movement | Layout changed |
| Postcondition | Verified state | Drop silently failed |

## Runnable example

```python
source = page.locator("[data-testid='source']")
target = page.locator("[data-testid='target']")
source.drag_to(target)
assert target.get_attribute("data-state") == "received"
print("drop verified")
```

## Failure modes

- Dragging by stale coordinates.
- Dropping into a destructive target without a boundary.
- Assuming the gesture succeeded without checking state.
- Using an untrusted locator without validation.

## Related

- mouse-input.md
- screenshot-capture.md
- assertion.md

## Evidence

- AI_CONSTITUTION.md
- AGENTS.md
- Repository security and validation workflows
