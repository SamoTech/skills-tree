# Drag and Drop

**Category:** `computer-use`
**Skill Level:** `intermediate`
**Stability:** `stable`

### Description

Click and hold on a source element, move to a target position, and release to perform a drag-and-drop operation. Used for file moves, reordering lists, and canvas operations.

### Example

```python
import pyautogui

# Drag file from (100, 200) to (500, 200)
pyautogui.dragTo(500, 200, duration=0.5, button='left')

# Or using drag from source to destination
pyautogui.drag(
    xOffset=400, yOffset=0,  # relative movement
    duration=0.5,
    button='left'
)
```

### Related Skills

- [Mouse Move](mouse-move.md)
- [Mouse Click](mouse-click.md)
- [Visual Element Detection](visual-element-detection.md)
