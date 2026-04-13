---
title: "Screenshot Capture"
category: 10-computer-use
level: basic
stability: stable
description: "Apply screenshot capture in AI agent workflows."
added: "2025-03"
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-10-computer-use-screenshot-capture.json)

# Screenshot Capture

**Category:** `computer-use`  
**Skill Level:** `basic`  
**Stability:** `stable`
**Added:** 2025-03

### Description

Capture a screenshot of the full screen, active window, or a specific region.

### Example

```python
import pyautogui
screenshot = pyautogui.screenshot(region=(0, 0, 1920, 1080))
screenshot.save('screen.png')
```

### Frameworks

- `pyautogui`, `mss`, `Pillow`
- Playwright `page.screenshot()`
- Anthropic Computer Use

### Related Skills

- [Screen Reading](../01-perception/screen-reading.md)
- [OCR](../01-perception/ocr.md)
- [Mouse Click](mouse-click.md)
