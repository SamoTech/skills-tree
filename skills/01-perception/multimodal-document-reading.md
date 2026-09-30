---
title: "Multimodal Document Reading"
category: 01-perception
level: intermediate
stability: stable
version: v2
description: "Process documents containing text, images, tables, and diagrams while preserving content order, page boundaries, and extraction provenance."
added: "2025-03"
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-01-perception-multimodal-document-reading.json)

# Multimodal Document Reading
Category: perception | Level: intermediate | Stability: stable | Version: v1

## Description
Process documents containing mixed content — text, images, tables, and diagrams — in a single parsing pass.

## Inputs
- `file`: PDF, DOCX, or PPTX path
- `extract_images`: bool

## Outputs
- Ordered content blocks: `{type: text|image|table, content, page}`

## Example
```python
from unstructured.partition.auto import partition
elements = partition(filename="report.pdf", strategy="hi_res", extract_images_in_pdf=True)
for el in elements:
    print(el.category, str(el)[:80])
```

## Frameworks
| Framework | Method |
|---|---|
| Python | `unstructured`, `pdfplumber` |
| LlamaIndex | `LlamaParse` |
| LangChain | `UnstructuredFileLoader` |

## Failure Modes
- Two-column PDFs read left-then-right across columns
- Embedded fonts corrupt text layer

## Related
- `pdf-parsing.md` · `image-understanding.md` · `table-extraction.md`

## Changelog
- v1 (2026-04): Initial entry


## Evidence

- https://docs.unstructured.io/open-source/core-functionality/partitioning
- https://python.langchain.com/docs/concepts/document_loaders/

Evidence status: these references support implementation guidance; no performance benchmark is claimed without reproducible benchmark data.
