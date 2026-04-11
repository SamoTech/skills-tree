# Keyboard Type

**Category:** `computer-use`  
**Skill Level:** `basic`  
**Stability:** `stable`

### Description

Simulate keyboard input — typing text strings or pressing individual keys at the current focus.

### Example

```python
import pyautogui
pyautogui.write('Hello, World!', interval=0.05)
pyautogui.press('enter')
pyautogui.hotkey('ctrl', 'c')  # Copy
```

### Related Skills

- [Mouse Click](mouse-click.md)
- [Keyboard Shortcut](keyboard-shortcut.md)
