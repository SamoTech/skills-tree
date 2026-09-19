---
title: "Document Parsing"
category: 01-perception
level: intermediate
stability: stable
description: "Parse documents into structured sections, paragraphs, tables, metadata, and source locations while preserving reading order and extraction uncertainty."
related: [text-reading, structured-data-reading, json-schema-validation]
added: "2025-03"
    min_version: "0.3.0"
    tested_version: "0.4.1"
    confidence: verified
    notes: "Patched PYSEC-2024-278. Use langchain-community>=0.4.1."
version: v2
updated: "2026-09"
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-01-perception-document-parsing.json)

# Document Parsing

## Description

Parse documents into structured sections, paragraphs, tables, metadata, and source locations while preserving reading order and extraction uncertainty.

## When to Use

Use for PDFs, word-processing files, HTML exports, reports, invoices, and other documents that need downstream retrieval or analysis.

## Inputs / Outputs

| Field | Type | Description |
|---|---|---|
| input | structured | Source content plus any format-specific metadata. |
| options | object | Limits, locale, schema, or provider-specific parsing options. |
| output | structured | Normalized records with provenance and explicit uncertainty. |

## Runnable Example

```python
from dataclasses import dataclass

@dataclass(frozen=True)
class Block:
    kind: str
    text: str
    page: int | None = None

def parse_blocks(raw: list[dict]) -> list[Block]:
    blocks = []
    for item in raw:
        text = str(item.get("text", "")).strip()
        if not text:
            continue
        blocks.append(Block(str(item.get("kind", "paragraph")), text, item.get("page")))
    return blocks

print(parse_blocks([
    {"kind": "heading", "text": "Invoice", "page": 1},
    {"kind": "paragraph", "text": "Total: 100", "page": 1},
]))
```

## Failure Modes

| Failure | Cause | Mitigation |
|---|---|---|
| Broken reading order | malformed or adversarial input | Validate structure before semantic processing. |
| OCR artifacts | unexpected source variation | Preserve raw context and emit a warning. |
| embedded objects | incomplete source | Mark uncertainty instead of inventing values. |
| Resource exhaustion | unbounded input | Enforce size, time, and result limits. |

## Output Contract

Ordered document blocks with type and source location; retain extraction warnings rather than silently repairing uncertain text.

## Design Rules

1. Preserve source provenance and ordering whenever it is available.
2. Validate structure before interpreting semantics.
3. Never silently convert uncertainty into a confident assertion.
4. Bound input size, execution time, and result cardinality.
5. Keep provider-specific parsing behind a stable internal representation.

## Related Skills

- [Text Reading](text-reading.md) — plain text extraction and normalization
- [Structured Data Reading](structured-data-reading.md) — schema-aware data ingestion
- [JSON Schema Validation](json-schema-validation.md) — validate normalized structures

## Changelog

| Version | Date | Change |
|---|---|---|
| v1 | 2025-03 | Initial skill entry |
| v2 | 2026-09 | Replaced placeholder guidance with executable implementation, I/O contract, failure modes, and bounded parsing rules |
