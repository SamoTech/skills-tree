---
title: "Drag and Drop"
category: 04-action-execution
level: intermediate
stability: stable
description: "Apply drag and drop in AI agent workflows."
added: "2025-03"
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-04-action-execution-drag-drop.json)

# Drag and Drop

**Category:** `action-execution`  
**Skill Level:** `intermediate`  
**Stability:** `stable`
**Added:** 2025-03

### Description

Simulate drag-and-drop interactions on a GUI — moving UI elements, files, or reordering items.

### Example

```python
import pyautogui
# Drag from (100, 200) to (400, 200) over 0.5 seconds
pyautogui.drag(300, 0, duration=0.5, button='left')
```

### Related Skills

- [Mouse Input](mouse-input.md)
- [Screenshot Capture](screenshot-capture.md)
