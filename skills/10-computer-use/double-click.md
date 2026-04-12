# Double Click

**Category:** `computer-use`
**Skill Level:** `basic`
**Stability:** `stable`

### Description

Double-click at a screen coordinate or on a detected UI element to open files, launch apps, or activate items that require a double-click event.

### Example

```python
import pyautogui

# Double-click to open a file
pyautogui.doubleClick(400, 300)

# Double-click with explicit interval between clicks
pyautogui.doubleClick(400, 300, interval=0.1)
```

### Related Skills

- [Mouse Click](mouse-click.md)
- [App Launch](app-launch.md)
- [Visual Element Detection](visual-element-detection.md)
