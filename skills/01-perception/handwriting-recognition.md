---
title: "Handwriting Recognition"
category: 01-perception
level: intermediate
stability: stable
description: "Apply handwriting recognition in AI agent workflows."
added: "2025-03"
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-01-perception-handwriting-recognition.json)

# Handwriting Recognition

**Category:** `perception`  
**Skill Level:** `intermediate`  
**Stability:** `stable`  
**Added:** 2025-03  
**Last Updated:** 2026-04

---

## Description

Transcribe handwritten text from images — notes, forms, signatures, whiteboard photos, and annotated diagrams. Handles cursive, print, mixed scripts, and poorly lit or skewed images. Goes beyond OCR by also interpreting crossed-out text, arrows, annotations, and layout hints (numbered lists, tables drawn by hand).

---

## Inputs

| Input | Type | Required | Description |
|---|---|---|---|
| `image` | `bytes` / `url` | ✅ | Image file containing handwriting |
| `context` | `string` | ❌ | Domain hint, e.g. `"medical intake form"` or `"math equations"` |
| `language` | `string` | ❌ | Expected language (default: auto-detect) |

---

## Outputs

| Output | Type | Description |
|---|---|---|
| `transcription` | `string` | Full verbatim text |
| `confidence` | `string` | `high` / `medium` / `low` |
| `illegible_sections` | `list` | Sections that were unclear |
| `layout_notes` | `string` | Structural observations (numbered list, table, etc.) |

---

## Example

```python
import anthropic
import base64
from pathlib import Path

client = anthropic.Anthropic()

def transcribe_handwriting(image_path: str, context: str = "") -> dict:
    """Transcribe handwritten text from an image."""
    image_data = base64.standard_b64encode(
        Path(image_path).read_bytes()
    ).decode("utf-8")

    suffix = Path(image_path).suffix.lower()
    media_map = {".jpg": "image/jpeg", ".jpeg": "image/jpeg",
                 ".png": "image/png", ".webp": "image/webp"}
    media_type = media_map.get(suffix, "image/png")

    prompt = (
        "Transcribe all handwritten text in this image exactly as written.\n"
        "Return JSON with:\n"
        "- transcription: full verbatim text\n"
        "- confidence: high | medium | low\n"
        "- illegible_sections: list of sections that were unclear\n"
        "- layout_notes: structural observations (numbered list, table, etc.)\n"
        "Return ONLY valid JSON."
    )
    if context:
        prompt += f"\n\nContext hint: {context}"

    response = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=1024,
        messages=[{
            "role": "user",
            "content": [
                {"type": "image", "source": {"type": "base64", "media_type": media_type, "data": image_data}},
                {"type": "text", "text": prompt}
            ]
        }]
    )
    return response.content[0].text

result = transcribe_handwriting("notes.jpg", context="medical intake form")
print(result)
```

---

## Frameworks & Models

| Framework / Model | Implementation | Since |
|---|---|---|
| Claude claude-opus-4-5 | Native vision via `image` content block | 2024-06 |
| GPT-4o | Vision via `image_url` | 2024-05 |

---

## Notes

- Providing domain context significantly improves accuracy
- Pre-process images: deskew, increase contrast, and upscale below 150 DPI before sending
- For multi-page documents, process page-by-page and concatenate results

---

## Related Skills

- [OCR](ocr.md) — printed text extraction
- [Image Understanding](image-understanding.md) — general image analysis
- [Document Parsing](document-parsing.md) — for full document pipelines

---

## Changelog

| Date | Change |
|---|---|
| `2026-04` | Expanded from stub: full description, I/O table, multi-format image example |
| `2025-03` | Initial stub entry |
