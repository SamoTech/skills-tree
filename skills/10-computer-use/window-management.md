---
title: "Window Management"
category: 10-computer-use
level: advanced
stability: stable
version: v2
description: "Move, resize, minimize, maximize, or focus a verified application window within explicit bounds."
added: "2025-03"
related: [multi-monitor, app-launch]
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-10-computer-use-window-management.json)

# Window Management

**Category:** `computer-use`
**Skill Level:** `advanced`
**Stability:** `stable`
**Added:** 2025-03

### Description

Move, resize, minimize, maximize, or focus a verified application window within explicit bounds. Window operations are contract-first: identify the exact window among same-titled candidates, apply the declared operation, and verify the resulting geometry rather than trusting the operation acknowledgement.

### Inputs / Outputs

| Direction | Field | Type | Contract |
|---|---|---|---|
| Input | window | object | The verified window identity (process, title, window id) |
| Input | operation | object | The declared move/resize/focus operation with target geometry |
| Output | geometry | object | The observed resulting window geometry and state |
| Output | check | object | Verification that the geometry matches the declared operation |

### Procedure
1. Enumerate matching windows and disambiguate when several share a title.
2. Apply the declared operation with target geometry validated against the display bounds.
3. Wait for window animations to settle before observing.
4. Verify the resulting geometry and state (position, size, focused, not minimized).
5. Stop and report when the operation failed or the window state is ambiguous (minimized windows have no usable geometry).

### Example

```python
window = {"id": "editor-main", "candidates": 1}
assert window["candidates"] == 1, "ambiguous window title requires disambiguation"
op = {"kind": "resize", "target": {"x": 100, "y": 100, "w": 1280, "h": 800}}
display = {"w": 2560, "h": 1440}
fits = op["target"]["x"] + op["target"]["w"] <= display["w"] and op["target"]["y"] + op["target"]["h"] <= display["h"]
assert fits, "target geometry exceeds display bounds"
result = {"state": "normal", "geometry": op["target"]}
assert result["state"] == "normal", "minimized windows have no usable geometry"
print({"window": window["id"], "operation": op["kind"], "geometry_verified": True})
```

### Related Skills

- [Multi Monitor](multi-monitor.md) - displays bound the geometry
- [App Launch](app-launch.md) - the launch that created the window
- [Tool Guardrails](../07-tool-use/tool-guardrails.md) - keep window operations within bounds

## Failure Modes

- Multiple windows share a title and the operation lands on the wrong one.
- Minimized windows have no usable geometry, so resize/focus silently no-ops.
- Window animations are still running when the geometry is verified.
- Maximize and full-screen are conflated, producing an unexpected state.
- The declared geometry exceeds display bounds or ignores the dock/taskbar reserved area.

## Changelog
- v2 (2026-11): Structural modernization; added the input/output contract table, a deterministic example, an execution procedure, and corpus-verified related links (replaced the non-corpus input-guardrails/output-guardrails/self-category pointers).
- v1 (2025-03): Initial entry.

## Evidence

- https://agentskills.io/specification

Evidence status: implementation guidance only; no benchmark claim is made without reproducible evidence.
