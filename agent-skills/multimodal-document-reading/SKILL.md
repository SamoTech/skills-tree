---
name: multimodal-document-reading
description: Process documents containing text, images, tables, and diagrams while preserving content order, page boundaries, and extraction provenance.
license: MIT
metadata:
  source: skills/01-perception/multimodal-document-reading.md
  version: "v2"
---

# Multimodal Document Reading

1. Detect the document format and available content layers.
2. Extract text, images, tables, and diagrams as separate typed elements.
3. Preserve page, slide, or sheet coordinates where supported.
4. Maintain reading order and mark uncertain ordering.
5. Route scanned or image-only regions through OCR or vision processing.
6. Return provenance for each extracted element.

## Failure modes

- Multi-column order errors: preserve layout coordinates and validate reading order.
- Missing text layer: use OCR and mark OCR-derived content.
- Embedded active content: treat macros/scripts as untrusted and never execute them during extraction.

## Evidence

- https://docs.unstructured.io/open-source/core-functionality/partitioning
- https://python.langchain.com/docs/concepts/document_loaders/
