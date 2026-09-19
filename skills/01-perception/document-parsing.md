---
title: "Document Parsing"
category: 01-perception
level: intermediate
stability: stable
description: "Parse documents into structured sections, paragraphs, tables, metadata, and source locations while preserving reading order and extraction uncertainty."
related: [text-reading, structured-data-reading, json-schema-validation]
added: "2025-03"
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

Input: a document source and an optional extraction policy. Output: ordered blocks with type, text or cell data, source location when available, and extraction warnings. Preserve page, section, or element identifiers when supplied by the parser.

## Runnable Example

```python
from pathlib import Path


def extract_text(path: str) -> dict:
    """Read a UTF-8 text fixture without silently accepting a missing source."""
    source = Path(path)
    if not source.is_file():
        raise FileNotFoundError(source)
    text = source.read_text(encoding="utf-8")
    return {"type": "document", "source": str(source), "text": text}

print(extract_text("example.txt"))
```

## Failure Modes

- Missing or unreadable source: fail explicitly with the source path or parser error.
- Unsupported format: report the format limitation instead of returning an empty successful result.
- Broken reading order: preserve source locations and flag the affected blocks.
- OCR uncertainty: retain extraction uncertainty and avoid silently correcting names, numbers, or legal text.
- Table extraction errors: preserve the raw region or warning when cell boundaries are uncertain.

## Output Contract

Every emitted block must identify its type and preserve its source order. Text blocks must contain non-empty text unless the parser explicitly represents an empty structural element. Source locations should be retained whenever the source parser provides them.

## Design Rules

Separate extraction from interpretation. Preserve page and element boundaries. Do not silently normalize source content that could change meaning. For high-value fields such as dates, amounts, identifiers, and legal clauses, retain the original text alongside normalized values.

## Related Skills

- `text-reading`
- `structured-data-reading`
- `json-schema-validation`

## Changelog

- v2 (2026-09): repaired malformed metadata and added bounded extraction guidance, output contract, and executable fixture example.
