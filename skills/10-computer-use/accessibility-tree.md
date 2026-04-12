# Accessibility Tree Navigation

**Category:** `computer-use`
**Skill Level:** `advanced`
**Stability:** `stable`
**Added:** 2025-03

### Description

Use OS accessibility APIs (AT-SPI on Linux, UIAutomation on Windows, AXUIElement on macOS) to navigate and interact with UI elements by role, name, or property — more reliable than pixel-based automation.

### Example

```python
# Windows: using pywinauto
from pywinauto import Application

app = Application(backend='uia').connect(title='Notepad')
win = app.top_window()

# Find element by name and type
text_area = win.child_window(control_type='Edit')
text_area.type_keys('Hello from accessibility tree!')

# Click a button by name
win.child_window(title='File', control_type='MenuItem').click_input()
```

### Related Skills

- [Visual Element Detection](visual-element-detection.md)
- [Mouse Click](mouse-click.md)
- [Screen Region OCR](screen-ocr.md)
