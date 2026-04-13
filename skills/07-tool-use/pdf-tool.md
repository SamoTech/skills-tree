---
title: "PDF Tool"
category: 07-tool-use
level: intermediate
stability: stable
description: "Apply pdf tool in AI agent workflows."
added: "2025-03"
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-07-tool-use-pdf-tool.json)

# PDF Tool

**Category:** `tool-use`  
**Skill Level:** `intermediate`  
**Stability:** `stable`
**Added:** 2025-03

### Description

Extract text, metadata, and tables from PDF files as an agent tool.

### Example

```python
import pdfplumber

def extract_pdf_text(path: str) -> str:
    with pdfplumber.open(path) as pdf:
        return '\n'.join(page.extract_text() or '' for page in pdf.pages)
```

### Related Skills

- [PDF Parsing](../01-perception/pdf-parsing.md)
- [Document Parsing](../01-perception/document-parsing.md)
