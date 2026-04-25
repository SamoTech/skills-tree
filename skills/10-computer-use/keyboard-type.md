---
title: "Keyboard Type"
category: 10-computer-use
level: basic
stability: stable
added: "2025-03"
description: "Apply keyboard typing in AI agent workflows."
dependencies:
  - package: pyautogui
    min_version: "0.9.54"
    tested_version: "0.9.54"
    confidence: verified
code_blocks:
  - id: "example-type"
    type: executable
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-10-computer-use-keyboard-type.json)

# Keyboard Type

**Category:** `computer-use`  
**Skill Level:** `basic`  
**Stability:** `stable`
**Added:** 2025-03

### Description

Type text and press individual keys or keyboard shortcuts programmatically.

### Example

```python
# pip install pyautogui
import pyautogui
import time

time.sleep(1)

# Type a string with a slight interval between characters
pyautogui.typewrite("Hello, world!", interval=0.05)

# Press a single key
pyautogui.press("enter")

# Press a hotkey combination
pyautogui.hotkey("ctrl", "a")  # select all
pyautogui.hotkey("ctrl", "c")  # copy
```

### Related Skills
- `keyboard-shortcut`, `mouse-click`, `form-filling`, `clipboard-write`
