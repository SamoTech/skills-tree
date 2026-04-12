# Terminal / Shell Interaction

**Category:** `computer-use`
**Skill Level:** `intermediate`
**Stability:** `stable`
**Added:** 2025-03

### Description

Type and execute shell commands in a terminal window by simulating keyboard input, then capture output via screenshot OCR or clipboard.

### Example

```python
import pyautogui
import time

# Focus terminal window
pyautogui.click(800, 600)  # terminal position
time.sleep(0.2)

# Type and run a command
pyautogui.typewrite('ls -la /home/user', interval=0.03)
pyautogui.press('enter')
time.sleep(0.5)

# Capture output via screenshot + OCR
from PIL import ImageGrab
import pytesseract
output = pytesseract.image_to_string(ImageGrab.grab())
```

### Related Skills

- [Screen Region OCR](screen-ocr.md)
- [Keyboard Type](keyboard-type.md)
- [Screenshot Capture](screenshot-capture.md)
