---
title: "Scroll"
category: 10-computer-use
level: basic
stability: stable
description: "Apply scroll in AI agent workflows."
added: "2025-03"
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-10-computer-use-scroll.json)

# Scroll

**Category:** `computer-use`
**Skill Level:** `basic`
**Stability:** `stable`
**Added:** 2025-03

### Description

Scroll a window, panel, or element vertically or horizontally to reveal content not visible in the current viewport.

### Example

```python
import pyautogui

# Scroll down 5 clicks at mouse position
pyautogui.scroll(-5)  # negative = down, positive = up

# Scroll at a specific position
pyautogui.scroll(3, x=400, y=300)  # scroll up at (400, 300)

# Horizontal scroll
pyautogui.hscroll(2)  # scroll right
```

### Related Skills

- [Mouse Move](mouse-move.md)
- [Browser Navigation](../11-web/browser-navigation.md)
- [Visual Element Detection](visual-element-detection.md)
