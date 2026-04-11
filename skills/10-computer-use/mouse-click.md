# Mouse Click

**Category:** `computer-use`  
**Skill Level:** `basic`  
**Stability:** `stable`

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
