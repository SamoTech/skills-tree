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
