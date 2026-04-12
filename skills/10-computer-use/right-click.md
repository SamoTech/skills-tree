# Right Click / Context Menu

**Category:** `computer-use`
**Skill Level:** `intermediate`
**Stability:** `stable`
**Added:** 2025-03

### Description

Right-click at a screen position or on a UI element to open a context menu, then select a menu item by text or position.

### Example

```python
import pyautogui

# Right-click on a file icon
pyautogui.rightClick(640, 480)

# Wait for context menu and click "Open With"
import time; time.sleep(0.3)
pyautogui.click(640, 510)  # "Open With" menu item position
```

### Related Skills

- [Mouse Click](mouse-click.md)
- [Accessibility Tree Navigation](accessibility-tree.md)
- [Visual Element Detection](visual-element-detection.md)
