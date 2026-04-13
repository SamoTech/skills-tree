---
title: "Mouse Move"
category: 10-computer-use
level: basic
stability: stable
description: "Apply mouse move in AI agent workflows."
added: "2025-03"
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-10-computer-use-mouse-move.json)

# Mouse Move

**Category:** `computer-use`
**Skill Level:** `basic`
**Stability:** `stable`
**Added:** 2025-03

### Description

Move the mouse cursor to an absolute screen coordinate or relative to its current position, without clicking. Used to hover over elements, reveal tooltips, or position before a click.

### Example

```python
import pyautogui

# Move to absolute position (x=500, y=300) over 0.3 seconds
pyautogui.moveTo(500, 300, duration=0.3)

# Move relative to current position
pyautogui.moveRel(100, -50, duration=0.2)
```

### Related Skills

- [Mouse Click](mouse-click.md)
- [Drag and Drop](drag-drop.md)
- [Screenshot Capture](screenshot-capture.md)
