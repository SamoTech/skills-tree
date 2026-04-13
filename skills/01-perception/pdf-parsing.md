![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-01-perception-pdf-parsing.json)

# PDF Parsing

**Category:** `perception`  
**Skill Level:** `basic`  
**Stability:** `stable`  
**Added:** 2025-03  
**Last Updated:** 2026-04

---

## Description

Extract text, tables, metadata, and structure from PDF documents. Handles both text-based PDFs (via `pypdf`) and scanned/image-based PDFs (via vision). Preserves section hierarchy, identifies tables, extracts form fields, and returns normalized structured output. Supports multi-page documents, multi-column layouts, and mixed content (text + images).

---

## Inputs

| Input | Type | Required | Description |
|---|---|---|---|
| `pdf_path` | `string` | ✅ | Local path or URL to the PDF file |
| `pages` | `list` | ❌ | Specific page numbers to extract (default: all) |
| `extract_tables` | `bool` | ❌ | Whether to extract tables as markdown (default: true) |

---

## Outputs

| Output | Type | Description |
|---|---|---|
| `text` | `string` | Extracted plain text |
| `tables` | `list` | Tables as markdown strings |
| `metadata` | `dict` | Title, author, page count, creation date |

---

## Example

```python
import anthropic
import base64
from pathlib import Path

client = anthropic.Anthropic()

def parse_pdf_document(pdf_path: str) -> str:
    """Extract structured content from a PDF using Claude's native PDF support."""
    pdf_data = base64.standard_b64encode(
        Path(pdf_path).read_bytes()
    ).decode("utf-8")

    response = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=4096,
        messages=[{
            "role": "user",
            "content": [
                {
                    "type": "document",
                    "source": {
                        "type": "base64",
                        "media_type": "application/pdf",
                        "data": pdf_data
                    }
                },
                {
                    "type": "text",
                    "text": (
                        "Extract and return JSON with:\n"
                        "- title: document title\n"
                        "- sections: [{heading, content}]\n"
                        "- tables: [markdown table strings]\n"
                        "- key_facts: list of important facts\n"
                        "Return ONLY valid JSON."
                    )
                }
            ]
        }]
    )
    return response.content[0].text

result = parse_pdf_document("invoice.pdf")
print(result)
```

```python
# Text-based PDFs: faster extraction with pypdf
import pypdf

def extract_text_pypdf(pdf_path: str) -> str:
    reader = pypdf.PdfReader(pdf_path)
    return "\n".join(page.extract_text() for page in reader.pages)
```

---

## Frameworks & Models

| Framework / Model | Implementation | Since |
|---|---|---|
| Claude claude-opus-4-5 | Native `document` content block for PDFs | 2024-06 |
| LangChain | `PyPDFLoader` + LLM chain | v0.1 |
| GPT-4o | Base64 image per page | 2024-05 |

---

## Notes

- Claude natively supports PDF documents via the `document` content block — no image conversion needed
- `pypdf` is preferred for digital PDFs when only raw text is needed (faster, cheaper)
- Split PDFs >50 pages into chunks to avoid context limits
- For scanned PDFs, Claude's vision handles OCR automatically via the `document` block

---

## Related Skills

- [Document Parsing](document-parsing.md) — general document extraction
- [OCR](ocr.md) — scanned/image text extraction
- [Image Understanding](image-understanding.md) — for image-heavy PDFs

---

## Changelog

| Date | Change |
|---|---|
| `2026-04` | Expanded from stub: native PDF document block example, pypdf fallback, notes |
| `2025-03` | Initial stub entry |
