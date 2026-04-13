![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-01-perception-document-parsing.json)

# Document Parsing

**Category:** `perception`  
**Skill Level:** `intermediate`  
**Stability:** `stable`  
**Added:** 2025-03  
**Version:** v2

---

## Description

Parse structured office documents — DOCX, XLSX, PPTX, HTML, CSV — extracting text, tables, images, and embedded metadata. Production systems must handle corrupt files, password-protected docs, mixed encodings, and scanned PDFs gracefully.

---

## Input / Output

| Input | Output |
|---|---|
| `.docx` / `.odt` | Paragraph list, table list, image refs, style map |
| `.xlsx` / `.csv` | Sheet names → DataFrame, formula values (not formulas) |
| `.pptx` | Slide-by-slide text + speaker notes + image captions |
| `.html` | Cleaned prose via Trafilatura or Readability |
| Mixed zip bundle | Per-file structured JSON |

---

## Implementation

### Python — DOCX

```python
from docx import Document
from docx.oxml.ns import qn

def parse_docx(path: str) -> dict:
    doc = Document(path)
    paragraphs = [p.text for p in doc.paragraphs if p.text.strip()]
    tables = []
    for table in doc.tables:
        rows = [[cell.text for cell in row.cells] for row in table.rows]
        tables.append(rows)
    return {"paragraphs": paragraphs, "tables": tables}
```

### Python — XLSX

```python
import openpyxl

def parse_xlsx(path: str) -> dict:
    wb = openpyxl.load_workbook(path, data_only=True)
    sheets = {}
    for name in wb.sheetnames:
        ws = wb[name]
        sheets[name] = [[cell.value for cell in row] for row in ws.iter_rows()]
    return sheets
```

### LangChain loaders

```python
from langchain_community.document_loaders import (
    Docx2txtLoader, UnstructuredExcelLoader, UnstructuredPowerPointLoader
)

loader = Docx2txtLoader("report.docx")
docs = loader.load()  # List[Document] with page_content + metadata
```

---

## Frameworks

| Library | Best For | Notes |
|---|---|---|
| `python-docx` | DOCX structure | Tables, styles, headers/footers |
| `openpyxl` | XLSX (no formulas) | `data_only=True` resolves cached values |
| `python-pptx` | PPTX slides | Per-slide text + notes |
| `unstructured` | Mixed document types | Unified API, handles edge cases |
| `trafilatura` | HTML → clean prose | Best-in-class noise removal |
| LangChain loaders | Agent integration | Wrap all of the above |

---

## Edge Cases

- **Password-protected files** — catch `BadZipFile` / `PermissionError`; prompt user for password via `msoffcrypto-tool`
- **Corrupt files** — wrap in try/except and fallback to `unstructured`
- **Scanned DOCX** (images only) — detect zero paragraphs, route to OCR pipeline
- **Mixed encodings** — use `chardet` to detect encoding before reading CSV
- **Merged table cells** — `python-docx` exposes merged cells via `cell.spans`

---

## Related Skills

- [PDF Parsing](pdf-parsing.md)
- [Structured Data Reading](structured-data-reading.md)
- [OCR](ocr.md)
- [Email Parsing](email-parsing.md)
