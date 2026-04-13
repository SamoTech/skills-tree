![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-10-computer-use-visual-element-detection.json)

# Visual Element Detection

**Category:** `computer-use`
**Skill Level:** `advanced`
**Stability:** `experimental`
**Added:** 2025-03

### Description

Detect UI elements (buttons, fields, icons) on screen using computer vision — template matching, YOLO-based object detection, or multimodal VLM analysis of screenshots.

### Example

```python
import pyautogui

# Template matching: find a button image on screen
location = pyautogui.locateOnScreen(
    'assets/submit_button.png',
    confidence=0.85
)
if location:
    pyautogui.click(pyautogui.center(location))

# Or use a VLM to identify element positions
# prompt: "Where is the Submit button? Return x,y coordinates."
```

### Related Skills

- [Screenshot Capture](screenshot-capture.md)
- [Screen Region OCR](screen-ocr.md)
- [Mouse Click](mouse-click.md)
