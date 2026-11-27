---
title: "Multi Monitor"
category: 10-computer-use
level: advanced
stability: stable
version: v2
description: "Identify and target a specific display in a multi-monitor environment using verified display geometry and application state."
added: "2025-03"
related: [window-management, screenshot-capture]
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-10-computer-use-multi-monitor.json)

# Multi Monitor

**Category:** `computer-use`
**Skill Level:** `advanced`
**Stability:** `stable`
**Added:** 2025-03

### Description

Identify and target a specific display in a multi-monitor environment using verified display geometry and application state. Every action is contract-first: resolve the actual display arrangement before acting, and verify which display a window or coordinate actually belongs to afterwards.

### Inputs / Outputs

| Direction | Field | Type | Contract |
|---|---|---|---|
| Input | display | object | The target display identity (index, name, or geometry) |
| Input | intent | object | The action on that display (move window, capture, place pointer) |
| Output | layout | object | The verified display arrangement (order, resolutions, scale factors) |
| Output | check | object | Verification that the action landed on the declared display |

### Procedure
1. Enumerate the live display arrangement (order, bounds, scale factors) rather than assuming a saved layout.
2. Resolve the target display from the declared identity against the live arrangement.
3. Perform the action with coordinates converted into the target display's space and scale.
4. Verify the result belongs to the declared display (window geometry, captured region).
5. Stop and report mismatch when displays moved, scales differ, or a window straddles two displays.

### Example

```python
layout = [
    {"id": "DP-1", "bounds": {"x": 0, "y": 0, "w": 2560, "h": 1440}, "scale": 1.0},
    {"id": "HDMI-0", "bounds": {"x": 2560, "y": 0, "w": 1920, "h": 1080}, "scale": 1.25},
]
target = "HDMI-0"
disp = next(d for d in layout if d["id"] == target)
point = {"x": 3000, "y": 200}  # global coordinates
on_target = disp["bounds"]["x"] <= point["x"] < disp["bounds"]["x"] + disp["bounds"]["w"]
assert on_target, "coordinate outside the declared target display"
local = {"x": (point["x"] - disp["bounds"]["x"]) / disp["scale"], "y": point["y"] / disp["scale"]}
print({"display": target, "local_point": local, "scale_applied": disp["scale"]})
```

### Related Skills

- [Window Management](window-management.md) - move windows onto the target display
- [Screenshot Capture](screenshot-capture.md) - capture a specific display
- [Computer Use Error Recovery](computer-use-error-recovery.md) - recover from layout surprises

## Failure Modes

- The saved display order does not match the live arrangement after a re-dock or reboot.
- Mixed DPI scales make unconverted global coordinates land on the wrong display.
- A display hot-plug re-arranges screens between observation and action.
- The target window straddles two displays and geometry checks are ambiguous.
- Coordinates resolve to a display that is off or asleep.

## Changelog
- v2 (2026-11): Structural modernization; added the input/output contract table, a deterministic example, an execution procedure, and corpus-verified related links (replaced the non-corpus input-guardrails/output-guardrails/self-category pointers).
- v1 (2025-03): Initial entry.

## Evidence

- https://agentskills.io/specification

Evidence status: implementation guidance only; no benchmark claim is made without reproducible evidence.
