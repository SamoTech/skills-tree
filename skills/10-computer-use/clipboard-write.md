# Clipboard Write

**Category:** `computer-use`
**Skill Level:** `basic`
**Stability:** `stable`
**Added:** 2025-03

### Description

Write content to the system clipboard so it can be pasted into any application. Useful for injecting data into GUI fields without simulating keystrokes.

### Example

```python
import pyperclip
import pyautogui

# Write to clipboard
pyperclip.copy("Hello from the agent!")

# Click target field and paste
pyautogui.click(400, 300)  # click input field
pyautogui.hotkey('ctrl', 'v')  # paste
```

### Related Skills

- [Clipboard Read](clipboard-read.md)
- [Keyboard Type](keyboard-type.md)
- [Keyboard Shortcut](keyboard-shortcut.md)
