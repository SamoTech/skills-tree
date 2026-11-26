---
title: "Multimodal Document Reading"
category: 01-perception
level: intermediate
stability: stable
version: v3
description: "Process documents containing text, images, tables, and diagrams while preserving content order, page boundaries, and extraction provenance."
related: []
added: "2025-03"
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-01-perception-multimodal-document-reading.json)

# Multimodal Document Reading

## Description
Process documents containing mixed content (text, images, tables, and diagrams) in a single parsing pass while preserving content order, page boundaries, and extraction provenance.

## When to Use
- Structured ingestion of PDF, DOCX, or PPTX files that mix text with images and tables
- Downstream pipelines that need page-ordered content blocks instead of flattened text
- Auditable extraction where every block must carry its source page

## Inputs / Outputs

| Direction | Field | Type | Contract |
|---|---|---|---|
| Input | `file` | path (PDF, DOCX, or PPTX) | Document to parse; must exist and be readable by the parser |
| Input | `extract_images` | bool | When true, embedded images are emitted as separate blocks |
| Input | `strategy` | `"fast"` or `"hi_res"` | Parsing depth; `hi_res` is slower but preserves table structure |
| Output | `blocks` | list of `{type, content, page}` | Ordered content blocks; `type` is `text`, `image`, or `table` |
| Output | `provenance` | page and element id per block | Source location retained for every emitted block |
| Output | `unparsed` | list of warnings | Elements the parser could not classify; surfaced, never dropped silently |

## Example
```python
# pip install unstructured
from unstructured.partition.auto import partition

def read_document(path: str, strategy: str = "hi_res") -> list[dict]:
    elements = partition(filename=path, strategy=strategy, extract_images_in_pdf=True)
    blocks = []
    for el in elements:
        blocks.append({
            "type": el.category,
            "content": str(el),
            "page": getattr(el.metadata, "page_number", None),
        })
    return blocks

for block in read_document("report.pdf")[:5]:
    print(block["type"], block["page"], str(block["content"])[:80])
```

## Frameworks
| Framework | Method |
|---|---|
| Python | `unstructured`, `pdfplumber` |
| LlamaIndex | `LlamaParse` |
| LangChain | `UnstructuredFileLoader` |

## Procedure
1. Confirm authorization to read the document and record its origin.
2. Select the parsing strategy from the document type and the downstream table needs.
3. Run the partitioner and collect ordered blocks with page metadata.
4. Verify block order against the document outline (headings, page numbers).
5. Route image and table blocks to the matching downstream skills (image understanding, table extraction).
6. Emit unparsed elements as warnings instead of discarding them.

## Failure Modes
- Two-column PDFs read left-then-right across columns: verify column order with a layout-aware parser before treating block order as reading order.
- Embedded or subsetted fonts corrupt the text layer: fall back to OCR for affected pages and record the substitution.
- Scanned pages without a text layer produce empty blocks: detect zero-text pages and route them to OCR explicitly.
- Very large documents exceed memory: process page ranges incrementally and merge the results.
- Encrypted or password-protected files fail mid-parse: check encryption before parsing and require credentials from the caller.

## Related
- [PDF Parsing](pdf-parsing.md)
- [Image Understanding](image-understanding.md)
- [Table Extraction](table-extraction.md)

## Changelog
- v3 (2026-11): Structural modernization; added the input/output contract table, procedure, and expanded failure modes, and removed the stale body metadata line that contradicted frontmatter.
- v1 (2026-04): Initial entry.

## Evidence

- https://docs.unstructured.io/open-source/core-functionality/partitioning
- https://python.langchain.com/docs/concepts/document_loaders/

Evidence status: these references support implementation guidance; no performance benchmark is claimed without reproducible benchmark data.
