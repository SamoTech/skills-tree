# Keyboard Input

**Category:** `action-execution`  
**Skill Level:** `basic`  
**Stability:** `stable`
**Added:** 2025-03

### Description

Simulate keyboard input — typing text strings, pressing individual keys, or triggering keyboard shortcuts.

### Example

```python
import pyautogui
pyautogui.write('Hello, Agent!', interval=0.05)
pyautogui.press('enter')
pyautogui.hotkey('ctrl', 's')  # Save
```

### Related Skills

- [Mouse Input](mouse-input.md)
- [Keyboard Type](../10-computer-use/keyboard-type.md)
