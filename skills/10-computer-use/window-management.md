# Window Management

**Category:** `computer-use`
**Skill Level:** `intermediate`
**Stability:** `stable`
**Added:** 2025-03

### Description

Open, close, minimize, maximize, resize, and move application windows. Enables agents to organize the desktop state before performing tasks.

### Example

```python
import pygetwindow as gw

# Find and activate a window by title
win = gw.getWindowsWithTitle('Notepad')[0]
win.activate()
win.maximize()

# Resize and move
win.resizeTo(1200, 800)
win.moveTo(0, 0)

# Minimize
win.minimize()
```

### Related Skills

- [App Launch](app-launch.md)
- [Screenshot Capture](screenshot-capture.md)
- [Multi-Monitor Support](multi-monitor.md)
