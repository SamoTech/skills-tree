---
title: "OCR (Optical Character Recognition)"
category: 01-perception
level: intermediate
stability: stable
description: "Apply ocr (optical character recognition) in AI agent workflows."
added: "2025-03"
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-01-perception-ocr.json)

# OCR (Optical Character Recognition)

**Category:** `perception`  
**Skill Level:** `intermediate`  
**Stability:** `stable`  
**Added:** 2025-03  
**Version:** v2

---

## Description

Extract text from images, scanned PDFs, and screenshots using optical character recognition. Modern OCR pipelines combine classical engines (Tesseract) with vision-language models for high-accuracy extraction across languages, layouts, and document types.

---

## Approaches

| Approach | Accuracy | Speed | Best For |
|---|---|---|---|
| Tesseract 5 (LSTM) | ⭐⭐⭐ | Fast | Clean, single-column docs |
| EasyOCR | ⭐⭐⭐⭐ | Medium | Multi-language, rotated text |
| PaddleOCR | ⭐⭐⭐⭐ | Fast | Dense layouts, CJK scripts |
| GPT-4o Vision | ⭐⭐⭐⭐⭐ | Slow | Complex layouts, handwriting |
| Claude Vision | ⭐⭐⭐⭐⭐ | Slow | Tables-in-images, receipts |
| Azure Form Recognizer | ⭐⭐⭐⭐⭐ | Medium | Forms, invoices, structured docs |

---

## Implementation

### Tesseract (local, free)

```python
import pytesseract
from PIL import Image
import cv2
import numpy as np

def ocr_image(path: str, lang: str = "eng") -> str:
    img = cv2.imread(path)
    # Preprocessing: grayscale + threshold
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)
    pil_img = Image.fromarray(thresh)
    return pytesseract.image_to_string(pil_img, lang=lang,
                                       config="--psm 6 --oem 3")
```

### Vision LLM (best accuracy)

```python
import base64
from anthropic import Anthropic

def ocr_with_claude(image_path: str) -> str:
    with open(image_path, "rb") as f:
        image_data = base64.standard_b64encode(f.read()).decode()
    client = Anthropic()
    message = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=2048,
        messages=[{
            "role": "user",
            "content": [
                {"type": "image", "source": {"type": "base64",
                 "media_type": "image/jpeg", "data": image_data}},
                {"type": "text", "text": "Extract all text from this image verbatim. Preserve layout and table structure using markdown."}
            ]
        }]
    )
    return message.content[0].text
```

---

## Preprocessing Best Practices

1. **Deskew** — correct rotation with `deskew` library or `cv2.getRotationMatrix2D`
2. **Denoise** — `cv2.fastNlMeansDenoising` before thresholding
3. **Upscale** — resize to ≥300 DPI equivalent (`cv2.resize` with `INTER_CUBIC`)
4. **Binarise** — Otsu thresholding for variable lighting
5. **Remove borders** — crop tight to text region

---

## Related Skills

- [Document Parsing](document-parsing.md)
- [PDF Parsing](pdf-parsing.md)
- [Handwriting Recognition](handwriting-recognition.md)
- [Image Understanding](image-understanding.md)
