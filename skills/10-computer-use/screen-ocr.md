# Screen Region OCR

**Category:** `computer-use`
**Skill Level:** `intermediate`
**Stability:** `stable`

### Description

Extract text from a defined region of the screen using Optical Character Recognition. Enables agents to read UI labels, dialog text, and content that isn't accessible via the accessibility tree.

### Example

```python
import pytesseract
from PIL import ImageGrab

# Capture a region: (left, top, right, bottom)
region = ImageGrab.grab(bbox=(100, 200, 800, 400))
text = pytesseract.image_to_string(region)
print(text)  # → "Invoice Total: $1,450.00"
```

### Related Skills

- [Screenshot Capture](screenshot-capture.md)
- [Visual Element Detection](visual-element-detection.md)
- [Accessibility Tree Navigation](accessibility-tree.md)
