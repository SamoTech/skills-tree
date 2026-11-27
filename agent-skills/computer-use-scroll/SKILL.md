---
name: computer-use-scroll
description: Scroll a verified UI container or viewport by a bounded amount and verify the resulting visible state.
metadata:
  source: skills/10-computer-use/scroll.md
  category: 10-computer-use
  version: "v2"
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-10-computer-use-scroll.json)

# Scroll

**Category:** `computer-use`
**Skill Level:** `advanced`
**Stability:** `stable`
**Added:** 2025-03

### Description

Scroll a verified UI container or viewport by a bounded amount and verify the resulting visible state. Scrolling is hover-dependent and easily misdirected: verify which container receives the scroll, bound the amount, and verify the target content actually became visible.

### Inputs / Outputs

| Direction | Field | Type | Contract |
|---|---|---|---|
| Input | container | object | The verified scrollable container or viewport that must receive the scroll |
| Input | amount | object | The bounded scroll (lines, pixels, pages) and direction |
| Output | viewport | object | The observed scroll position after the action |
| Output | check | object | Verification that the intended content is now visible |

### Procedure
1. Verify the scrollable container and ensure the pointer hovers over it (not an inner pane).
2. Apply the bounded scroll amount in the declared direction.
3. Wait for scrolling (smooth-scroll or momentum) to settle before observing.
4. Verify the intended content is visible in the resulting viewport.
5. Stop and report when the wrong container scrolled or the target content never appears.

### Example

```python
scroll = {"container": "results-pane", "amount": {"direction": "down", "px": 600},
          "pointer_over": "results-pane"}
assert scroll["pointer_over"] == scroll["container"], "scroll would hit the wrong container"
after = {"scroll_top": 1450, "visible_target": "result-row-42"}
assert after["visible_target"] == "result-row-42", "target content not visible after scroll"
print({"scrolled": True, "container": scroll["container"], "target_visible": True})
```

### Related Skills

- [UI Element Waiting](ui-element-waiting.md) - wait for content to render after scrolling
- [Visual Element Detection](visual-element-detection.md) - confirm the target became visible
- [Computer Use Error Recovery](computer-use-error-recovery.md) - recover from scroll dead ends

## Failure Modes

- The scroll lands on an inner or outer pane because the pointer hovered the wrong element.
- Smooth scrolling or momentum is still in motion when the postcondition is checked.
- An unbounded feed has no end state and scrolling never terminates.
- Content virtualization removes rows above the viewport, invalidating element positions.
- The scroll amount overshoots and the target element leaves the viewport again.

## Changelog
- v2 (2026-11): Structural modernization; added the input/output contract table, a deterministic example, an execution procedure, and corpus-verified related links (replaced the non-corpus input-guardrails/output-guardrails/self-category pointers).
- v1 (2025-03): Initial entry.

## Evidence

- https://agentskills.io/specification

Evidence status: implementation guidance only; no benchmark claim is made without reproducible evidence.
