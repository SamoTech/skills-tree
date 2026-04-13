---
title: "File Dialog Interaction"
category: 10-computer-use
level: intermediate
stability: stable
description: "Apply file dialog interaction in AI agent workflows."
added: "2025-03"
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-10-computer-use-file-dialog.json)

# File Dialog Interaction

**Category:** `computer-use`
**Skill Level:** `intermediate`
**Stability:** `stable`
**Added:** 2025-03

### Description

Navigate OS file open/save dialogs by typing file paths directly into the dialog or interacting with the folder tree, enabling automated file selection without knowing exact pixel coordinates.

### Example

```python
import pyautogui
import time

# Trigger open dialog (e.g., Ctrl+O in an app)
pyautogui.hotkey('ctrl', 'o')
time.sleep(0.5)

# On Windows: type path in filename field
pyautogui.hotkey('ctrl', 'l')  # focus address bar
pyautogui.typewrite('C:\\Users\\user\\Documents\\report.pdf', interval=0.02)
pyautogui.press('enter')
```

### Related Skills

- [Keyboard Type](keyboard-type.md)
- [Keyboard Shortcut](keyboard-shortcut.md)
- [Terminal / Shell Interaction](terminal-interaction.md)
