# Document Parsing

**Category:** `perception`  
**Skill Level:** `intermediate`  
**Stability:** `stable`

### Description

Parse structured office documents: DOCX, XLSX, PPTX, HTML, CSV — extracting text, tables, and metadata.

### Example

```python
from docx import Document
doc = Document('report.docx')
for para in doc.paragraphs:
    print(para.text)
```

### Frameworks

- Python `python-docx`, `openpyxl`, `python-pptx`
- LangChain document loaders
- Unstructured.io

### Related Skills

- [PDF Parsing](pdf-parsing.md)
- [Structured Data Reading](structured-data-reading.md)
