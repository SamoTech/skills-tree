---
name: mouse-input
description: Perform bounded pointer actions against verified interface targets and verify consequential results instead of trusting coordinates.
metadata:
  source: skills/04-action-execution/mouse-input.md
  category: 04-action-execution
  version: "v2"
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-04-action-execution-mouse-input.json)

# Mouse Input

**Category:** `action-execution`
**Skill Level:** `intermediate`
**Stability:** `stable`
**Added:** 2026-09

### Description

Perform bounded pointer actions against verified interface targets and verify consequential results. Clicks target resolved elements rather than raw coordinates, destructive clicks require explicit authorization, and every consequential action is confirmed from the resulting state.

### Inputs / Outputs

| Direction | Field | Type | Contract |
|---|---|---|---|
| Input | `target` | element locator or bounded coordinates | What receives the pointer action; resolved before acting |
| Input | `action` | `click\|double_click\|right_click\|hover` | The pointer gesture to perform |
| Input | `authorized_destructive` | boolean | Must be true for any action with destructive effect |
| Output | `action_result` | `{performed, verified}` | Whether the gesture ran and the result was confirmed |
| Output | `observed_state` | string | The post-action state read from the interface |

### Procedure
1. Resolve the target element and confirm it is visible and enabled; prefer locators over absolute coordinates.
2. Classify the action: if it can delete, submit, spend, or send, require explicit authorization before performing it.
3. Perform exactly one gesture; avoid rapid repeated clicks that can double-trigger handlers.
4. Read the resulting state from the interface (attribute, panel, confirmation message) to verify the effect.
5. If the state did not change as expected, stop and report; do not retry the gesture blindly.
6. Keep hover and move actions bounded to the viewport of the resolved target.

### Example

```python
def click_verified(target, expected_attr: tuple[str, str]) -> dict:
    if not (target.is_visible() and target.is_enabled()):
        raise RuntimeError("target not interactable")
    target.click()
    attr, expected = expected_attr
    actual = target.get_attribute(attr)
    return {"performed": True, "verified": actual == expected,
            "observed_state": actual or "unchanged"}

result = click_verified(page.locator("[data-testid='save']"), ("data-state", "saved"))
print(result)
```

### Related Skills

- [Keyboard Input](keyboard-input.md)
- [Screenshot Capture](screenshot-capture.md)
- [Assertion](assertion.md)

## Failure Modes

- Stale coordinates after a layout change: re-resolve the target before each gesture.
- Clicking the wrong element when locators match multiple nodes: use a locator that resolves to exactly one element.
- Destructive clicks without an authorization check.
- Silent failure: the gesture completes but the interface state never changed and nobody checked.
- Double-triggering through impatient repeated clicks; verify once, then wait or investigate.

## Changelog
- v2 (2026-11): Structural modernization; added the input/output contract table, an explicit procedure, a deterministic verification example, expanded failure modes, and version history.
- v1 (2026-09): Initial entry.

## Evidence

- https://agentskills.io/specification

Evidence status: implementation guidance only; no benchmark claim is made without reproducible evidence.
