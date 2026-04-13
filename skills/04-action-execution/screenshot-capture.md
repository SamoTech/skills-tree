---
title: "Screenshot Capture (Action)"
category: 04-action-execution
level: basic
stability: stable
description: "Apply screenshot capture (action) in AI agent workflows."
added: "2025-03"
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-04-action-execution-screenshot-capture.json)

# Screenshot Capture (Action)

**Category:** `action-execution`  
**Skill Level:** `basic`  
**Stability:** `stable`
**Added:** 2025-03

### Description

Capture the current state of the screen as an image for visual verification, logging, or downstream visual reasoning.

### Example

```python
import pyautogui
shot = pyautogui.screenshot()
shot.save('state_snapshot.png')
```

### Related Skills

- [Screenshot Capture (Computer Use)](../10-computer-use/screenshot-capture.md)
- [Screen OCR](../10-computer-use/screen-ocr.md)
