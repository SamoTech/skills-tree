---
title: "PDF Parsing"
category: 01-perception
level: intermediate
stability: stable
description: "Extract text, tables, and metadata from PDF files in AI agent workflows."
added: "2025-03"
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-01-perception-pdf-parsing.json)

# PDF Parsing
Category: perception | Level: intermediate | Stability: stable | Version: v1

## Description
Extract structured text, tables, images, and metadata from PDF documents. Handles both native-text and scanned PDFs (via OCR fallback).

## Inputs
- `file_path`: path to PDF file
- `pages`: optional list of page numbers to extract
- `extract_tables`: boolean flag

## Outputs
- Dict with `text`, `tables`, `metadata`, and per-page content

## Example
```python
from pypdf import PdfReader
def parse_pdf(path):
    reader = PdfReader(path)
    return {
        "metadata": dict(reader.metadata),
        "pages": [page.extract_text() for page in reader.pages]
    }
```

## Frameworks
| Framework | Method |
|---|---|
| Python | `pypdf`, `pdfminer.six`, `pymupdf` |
| LlamaIndex | `PDFReader`, `LlamaParse` |
| LangChain | `PyPDFLoader`, `UnstructuredPDFLoader` |

## Dependencies
- package: pypdf
  tested_version: "5.4.0"
  confidence: verified
  notes: "Patched GHSA-4pxv-j86v-mhcw, GHSA-7gw9-cf7v-778f, GHSA-x284-j5p8-9c5p (infinite loop / DoS via crafted PDF). Use pypdf>=5.4.0."

## Failure Modes
- Scanned PDFs without OCR layer return empty text
- Password-protected files raise `PdfReadError`
- Malformed PDFs may hang on extraction — set timeout

## Related
- `document-parsing.md` · `ocr.md` · `table-extraction.md`

## Changelog
- v1 (2026-02): Initial entry
- v1.1 (2026-05): Bump pypdf to 5.4.0 (CVE patch)
