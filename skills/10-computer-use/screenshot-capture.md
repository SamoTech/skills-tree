---
title: "Screenshot Capture"
category: 10-computer-use
level: basic
stability: stable
added: "2025-03"
description: "Apply screenshot capture in AI agent workflows."
dependencies:
  - package: pyautogui
    min_version: "0.9.54"
    tested_version: "0.9.54"
    confidence: verified
  - package: Pillow
    min_version: "10.0.0"
    tested_version: "12.2.0"
    confidence: verified
code_blocks:
  - id: "example-screenshot"
    type: executable
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-10-computer-use-screenshot-capture.json)

# Screenshot Capture

**Category:** `computer-use`  
**Skill Level:** `basic`  
**Stability:** `stable`
**Added:** 2025-03

### Description

Capture full-screen or region screenshots for visual inspection, OCR pipelines, or feeding to vision models.

### Example

```python
# pip install pyautogui Pillow
import pyautogui
from PIL import Image
import io

# Full screen screenshot
screenshot = pyautogui.screenshot()
screenshot.save("screen.png")

# Capture a specific region (left, top, width, height)
region = pyautogui.screenshot(region=(0, 0, 800, 600))
region.save("region.png")

# Get as bytes for API calls
buf = io.BytesIO()
screenshot.save(buf, format="PNG")
image_bytes = buf.getvalue()
```

### Related Skills
- `screen-reading`, `screen-ocr`, `visual-element-detection`, `mouse-click`
