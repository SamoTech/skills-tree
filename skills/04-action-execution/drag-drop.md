# Drag and Drop

**Category:** `action-execution`  
**Skill Level:** `intermediate`  
**Stability:** `stable`

### Description

Simulate drag-and-drop interactions on a GUI — moving UI elements, files, or reordering items.

### Example

```python
import pyautogui
# Drag from (100, 200) to (400, 200) over 0.5 seconds
pyautogui.drag(300, 0, duration=0.5, button='left')
```

### Related Skills

- [Mouse Input](mouse-input.md)
- [Screenshot Capture](screenshot-capture.md)
