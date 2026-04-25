---
title: "OCR (Optical Character Recognition)"
category: 01-perception
level: intermediate
stability: stable
added: "2025-03"
updated: "2026-04"
version: v3
description: "Extract text from images and scanned documents. Modern stack: a vision-language model (Claude / GPT-4o) for layout-aware OCR, with Tesseract as the open-source fallback for high-volume / offline runs."
tags: [perception, vision, document, extraction, multimodal]
dependencies:
  - package: anthropic
    min_version: "0.39.0"
    tested_version: "0.39.0"
    confidence: verified
code_blocks:
  - id: "example-ocr"
    type: executable
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-01-perception-ocr.json)

# OCR (Optical Character Recognition)

## Description

OCR converts an **image of text** into machine-readable text. Classical OCR (Tesseract, AWS Textract) gives you raw characters with bounding boxes; **vision-language model OCR** (Claude, GPT-4o, Gemini) gives you structured output that respects layout — tables stay tables, columns stay columns, headers stay headers. The two approaches now coexist: VLM for structure-sensitive jobs, classical for high-volume / offline / cost-sensitive batch.

This skill returns both the raw text and a structured representation, plus per-page confidence so the caller can route low-confidence pages to a human review queue.

## When to Use

- The source is an **image** (scanned PDF, photo, screenshot) — not searchable PDF or HTML.
- You need text *plus* layout (forms, invoices, receipts, tables) → use VLM-OCR.
- You need raw text at low cost across many millions of pages → use Tesseract / Textract.
- **Don't use** when the file is a digital PDF (use [PDF Parsing](pdf-parsing.md)) or HTML (use [HTML Reading](html-reading.md)) — those have native text already.

## Inputs / Outputs

| Field | Type | Description |
|---|---|---|
| `image` | `bytes \| str` | Image bytes or path |
| `mode` | `Literal["raw","structured"]` | Plain text vs JSON-with-fields |
| `language` | `str` | ISO code; helps both VLM and Tesseract |
| → `text` | `str` | Raw extracted text |
| → `fields` | `dict \| None` | Structured fields (in `structured` mode) |
| → `confidence` | `float` | Self-rated 0–1; route < 0.7 to review |

## Runnable Example

```python
# pip install anthropic
from __future__ import annotations
import base64
import json
from dataclasses import dataclass
from pathlib import Path
import anthropic

client = anthropic.Anthropic()
MODEL = "claude-opus-4-5"

@dataclass
class OcrResult:
    text: str
    fields: dict | None
    confidence: float

SYSTEM_RAW = (
    "Transcribe the text in the image VERBATIM. Preserve line breaks, columns, "
    "and tables (use Markdown for tables). Output ONLY the transcription."
)

SYSTEM_STRUCTURED = (
    "Extract the document's content and key fields. Output a JSON object with "
    "keys: 'text' (full transcription, Markdown), 'fields' (object of "
    "field_name -> value, e.g. invoice_number, total, date, vendor), and "
    "'confidence' (your self-rated 0..1). Output ONLY JSON."
)

def _image_block(image: bytes | str) -> dict:
    if isinstance(image, str):
        image = Path(image).read_bytes()
    return {
        "type": "image",
        "source": {
            "type": "base64",
            "media_type": "image/png",
            "data": base64.b64encode(image).decode(),
        },
    }

def ocr(
    image: bytes | str,
    *,
    mode: str = "structured",
    language: str = "en",
) -> OcrResult:
    system = SYSTEM_STRUCTURED if mode == "structured" else SYSTEM_RAW
    r = client.messages.create(
        model=MODEL, max_tokens=4096, temperature=0.0,
        system=f"{system}\nLanguage hint: {language}.",
        messages=[{
            "role": "user",
            "content": [
                _image_block(image),
                {"type": "text", "text": "OCR this document."},
            ],
        }],
    )
    raw = r.content[0].text.strip()
    if mode == "structured":
        try:
            obj = json.loads(raw)
            return OcrResult(
                text=obj.get("text", ""),
                fields=obj.get("fields"),
                confidence=float(obj.get("confidence", 0.0)),
            )
        except json.JSONDecodeError:
            return OcrResult(text=raw, fields=None, confidence=0.5)
    return OcrResult(text=raw, fields=None, confidence=0.9)

if __name__ == "__main__":
    import sys
    out = ocr(sys.argv[1], mode="structured")
    print(f"confidence={out.confidence:.2f}")
    print("---")
    print(out.text[:500])
    if out.fields:
        print("---")
        print(json.dumps(out.fields, indent=2))
```

## Failure Modes

| Failure | Cause | Mitigation |
|---|---|---|
| Hallucinated text on blank/noisy regions | Low signal in image | Pre-filter with edge density; require min content; flag low-confidence |
| Wrong language detected | Auto-detect failed | Pass `language` hint explicitly |
| Tables flattened into a stream of words | Used raw mode for tabular data | Use structured mode with explicit table-as-Markdown instruction |
| Field names drift across runs | Free-form structured prompt | Provide a JSON schema with required field names; validate output |
| Low confidence not surfaced | Model self-rated optimistically | Cross-check with a second model; or with classical OCR + agreement |
| Cost spike | High-res images at scale | Downscale to 1024px max edge; use Haiku/Tesseract for low-stakes pages |

## Variants

| Variant | When |
|---|---|
| **VLM-OCR** (above) | Default for forms, invoices, receipts, mixed-layout |
| **Tesseract** | Open-source, offline, high-volume — but no layout understanding |
| **AWS Textract / Azure Document Intelligence** | Production document AI with built-in form/table extractors |
| **Two-stage**: Tesseract → LLM for structure | Cost-efficient: cheap raw, expensive structure |
| **Schema-grounded** | Pass a Pydantic schema; force structured output to match |

## Frameworks & Models

| Framework | Notes |
|---|---|
| Direct API (above) | Best layout, highest cost |
| `pytesseract` | Free, fast, no layout |
| AWS Textract | Strong on forms & tables; per-page billing |
| Azure Document Intelligence | Pre-built extractors for invoices, receipts, IDs |
| Google Document AI | Multilingual; pre-trained processors |

## Model Comparison

| Capability | claude-opus-4-5 | gpt-4o | claude-haiku-4-5 |
|---|---|---|---|
| Handwriting | 4 | 4 | 3 |
| Tables / forms layout | 5 | 5 | 4 |
| Multilingual | 4 | 5 | 4 |
| Cost-per-page | 2 | 3 | 5 |

## Related Skills

- [Image Understanding](image-understanding.md) — beyond text: charts, diagrams, photos
- [PDF Parsing](pdf-parsing.md) — for digital PDFs (no OCR needed)
- [Handwriting Recognition](handwriting-recognition.md) — sub-skill for cursive / forms
- [Table Extraction](table-extraction.md) — when the goal is the table, not the text

## Changelog

| Date | Version | Change |
|---|---|---|
| 2025-03 | v1 | Stub |
| 2026-04 | v3 | Battle-tested: VLM + classical, structured/raw modes, confidence routing, model comparison |
