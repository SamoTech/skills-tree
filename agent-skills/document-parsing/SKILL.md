---
name: document-parsing
description: Extract text, tables, and metadata from office and web documents with format-specific parsers and explicit handling for corrupt, protected, scanned, and mixed-content files.
license: MIT
metadata:
  source: skills/01-perception/document-parsing.md
  version: "v2"
---

# Document Parsing

1. Detect the document format before choosing a parser.
2. Extract text, tables, metadata, and embedded media separately.
3. Preserve page, slide, sheet, or paragraph boundaries when available.
4. Detect corrupt, protected, scanned, and image-only inputs and route them to the appropriate fallback.
5. Keep parser dependencies pinned and review known security advisories.
6. Return provenance for extracted content.

## Failure modes

- Corrupt archive: catch parser errors and stop rather than guessing.
- Scanned/image-only document: route to OCR and mark OCR-derived content.
- Formula or rendering differences: distinguish cached values from formulas and rendered output.

## Evidence

- https://python-docx.readthedocs.io/
- https://openpyxl.readthedocs.io/
- https://python.langchain.com/docs/concepts/document_loaders/
