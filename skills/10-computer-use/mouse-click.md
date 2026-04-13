![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-10-computer-use-mouse-click.json)

# Mouse Click

**Category:** `computer-use`  
**Skill Level:** `basic`  
**Stability:** `stable`
**Added:** 2025-03

### Description

Simulate a mouse click at specified screen coordinates or on a detected UI element.

### Example

```python
import pyautogui
pyautogui.click(x=960, y=540)  # Click center of 1080p screen
pyautogui.click('Submit')      # Click by button text (pyautogui locateOnScreen)
```

### Related Skills

- [Mouse Move](mouse-move.md)
- [Screenshot Capture](screenshot-capture.md)
- [Keyboard Type](keyboard-type.md)
