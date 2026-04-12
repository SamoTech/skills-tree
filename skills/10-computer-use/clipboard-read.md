# Clipboard Read

**Category:** `computer-use`
**Skill Level:** `basic`
**Stability:** `stable`
**Added:** 2025-03

### Description

Read the current content of the system clipboard. Used to retrieve text, URLs, or other data that a user or agent previously copied.

### Example

```python
import pyperclip

# Read clipboard content
content = pyperclip.paste()
print(content)  # → "https://github.com/SamoTech/skills-tree"

# Or use keyboard shortcut to copy then read
import pyautogui
pyautogui.hotkey('ctrl', 'a')  # select all
pyautogui.hotkey('ctrl', 'c')  # copy
content = pyperclip.paste()
```

### Related Skills

- [Clipboard Write](clipboard-write.md)
- [Keyboard Shortcut](keyboard-shortcut.md)
- [Keyboard Type](keyboard-type.md)
