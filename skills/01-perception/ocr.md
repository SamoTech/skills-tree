# OCR (Optical Character Recognition)

**Category:** `perception`  
**Skill Level:** `intermediate`  
**Stability:** `stable`

### Description

Extract text from images, scanned PDFs, and photos using OCR engines or vision-language models.

### Example

```python
import pytesseract
from PIL import Image
text = pytesseract.image_to_string(Image.open('scan.png'))
```

### Frameworks

- `pytesseract` (Tesseract wrapper)
- Google Cloud Vision API
- Azure AI Document Intelligence
- GPT-4o / Claude 3.7 (vision-based OCR)

### Related Skills

- [PDF Parsing](pdf-parsing.md)
- [Screen Reading](screen-reading.md)
- [Document Parsing](document-parsing.md)
