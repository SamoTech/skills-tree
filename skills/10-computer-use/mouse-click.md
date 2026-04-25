---
title: "Mouse Click"
category: 10-computer-use
level: basic
stability: stable
added: "2025-03"
description: "Apply mouse click in AI agent workflows."
dependencies:
  - package: pyautogui
    min_version: "0.9.54"
    tested_version: "0.9.54"
    confidence: verified
code_blocks:
  - id: "example-click"
    type: executable
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-10-computer-use-mouse-click.json)

# Mouse Click

**Category:** `computer-use`  
**Skill Level:** `basic`  
**Stability:** `stable`
**Added:** 2025-03

### Description

Perform left, right, and double mouse clicks at screen coordinates or on located UI elements.

### Example

```python
# pip install pyautogui
import pyautogui
import time

pyautogui.FAILSAFE = True  # move mouse to corner to abort
time.sleep(1)  # give time to switch windows

# Click at absolute coordinates
pyautogui.click(500, 300)

# Right-click
pyautogui.rightClick(500, 300)

# Double-click
pyautogui.doubleClick(500, 300)

# Click relative to current position
pyautogui.moveRel(100, 0, duration=0.3)
pyautogui.click()
```

### Related Skills
- `mouse-move`, `double-click`, `right-click`, `screenshot-capture`, `visual-element-detection`
