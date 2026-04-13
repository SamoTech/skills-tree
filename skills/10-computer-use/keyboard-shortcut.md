![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-10-computer-use-keyboard-shortcut.json)

# Keyboard Shortcut

**Category:** `computer-use`
**Skill Level:** `basic`
**Stability:** `stable`
**Added:** 2025-03

### Description

Execute keyboard shortcuts (e.g., Ctrl+C, Cmd+V, Alt+F4) to trigger application commands without using the mouse or menus.

### Example

```python
import pyautogui

# Copy selected text
pyautogui.hotkey('ctrl', 'c')

# Paste
pyautogui.hotkey('ctrl', 'v')

# Save file
pyautogui.hotkey('ctrl', 's')

# macOS equivalent
pyautogui.hotkey('command', 'c')
```

### Common Shortcuts

| Action | Windows/Linux | macOS |
|---|---|---|
| Copy | `Ctrl+C` | `Cmd+C` |
| Paste | `Ctrl+V` | `Cmd+V` |
| Undo | `Ctrl+Z` | `Cmd+Z` |
| Save | `Ctrl+S` | `Cmd+S` |
| Select All | `Ctrl+A` | `Cmd+A` |
| Close Window | `Alt+F4` | `Cmd+W` |

### Related Skills

- [Keyboard Type](keyboard-type.md)
- [Clipboard Read](clipboard-read.md)
- [Clipboard Write](clipboard-write.md)
