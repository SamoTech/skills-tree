# PDF Parsing

**Category:** `perception`  
**Skill Level:** `basic`  
**Stability:** `stable`
**Added:** 2025-03

### Description

Extract text, tables, and metadata from PDF documents, preserving structure where possible.

### Example

```python
from pypdf import PdfReader
reader = PdfReader('document.pdf')
for page in reader.pages:
    print(page.extract_text())
```

### Frameworks

- Python `pypdf`, `pdfminer`, `pdfplumber`
- LangChain `PyPDFLoader`
- Adobe PDF Extract API

### Related Skills

- [Document Parsing](document-parsing.md)
- [OCR](ocr.md)
