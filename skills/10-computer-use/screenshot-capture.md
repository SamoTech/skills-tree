# Screenshot Capture

**Category:** `computer-use`  
**Skill Level:** `basic`  
**Stability:** `stable`

### Description

Capture a screenshot of the full screen, active window, or a specific region.

### Example

```python
import pyautogui
screenshot = pyautogui.screenshot(region=(0, 0, 1920, 1080))
screenshot.save('screen.png')
```

### Frameworks

- `pyautogui`, `mss`, `Pillow`
- Playwright `page.screenshot()`
- Anthropic Computer Use

### Related Skills

- [Screen Reading](../01-perception/screen-reading.md)
- [OCR](../01-perception/ocr.md)
- [Mouse Click](mouse-click.md)
