---
title: "Keyboard Type"
category: 10-computer-use
level: basic
stability: stable
description: "Apply keyboard type in AI agent workflows."
added: "2025-03"
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-10-computer-use-keyboard-type.json)

# Keyboard Type

**Category:** `computer-use`  
**Skill Level:** `basic`  
**Stability:** `stable`
**Added:** 2025-03

### Description

Simulate keyboard input — typing text strings or pressing individual keys at the current focus.

### Example

```python
import pyautogui
pyautogui.write('Hello, World!', interval=0.05)
pyautogui.press('enter')
pyautogui.hotkey('ctrl', 'c')  # Copy
```

### Related Skills

- [Mouse Click](mouse-click.md)
- [Keyboard Shortcut](keyboard-shortcut.md)
