# Multi-Monitor Support

**Category:** `computer-use`
**Skill Level:** `advanced`
**Stability:** `stable`
**Added:** 2025-03

### Description

Detect, navigate, and capture content across multiple physical or virtual monitors. Enables agents to operate across extended desktops and multi-display setups.

### Example

```python
from screeninfo import get_monitors
import pyautogui

# List all monitors
for m in get_monitors():
    print(f"Monitor: {m.name} @ ({m.x},{m.y}) size {m.width}x{m.height}")

# Move mouse to second monitor (offset by first monitor width)
second_monitor_x = 1920 + 500  # assuming first monitor is 1920px wide
pyautogui.moveTo(second_monitor_x, 300)

# Capture specific monitor region
from PIL import ImageGrab
monitor2_region = ImageGrab.grab(bbox=(1920, 0, 3840, 1080))
```

### Related Skills

- [Screenshot Capture](screenshot-capture.md)
- [Window Management](window-management.md)
- [Mouse Move](mouse-move.md)
