![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-10-computer-use-app-launch.json)

# Application Launch

**Category:** `computer-use`
**Skill Level:** `basic`
**Stability:** `stable`
**Added:** 2025-03

### Description

Open a desktop application by name, path, or system command. Waits for the window to appear before continuing.

### Example

```python
import subprocess
import time
import pygetwindow as gw

# Launch Notepad on Windows
subprocess.Popen(['notepad.exe'])
time.sleep(1)  # wait for window
window = gw.getWindowsWithTitle('Notepad')[0]
window.activate()

# Launch app on macOS
subprocess.Popen(['open', '-a', 'TextEdit'])
```

### Related Skills

- [Window Management](window-management.md)
- [Terminal / Shell Interaction](terminal-interaction.md)
- [Screenshot Capture](screenshot-capture.md)
