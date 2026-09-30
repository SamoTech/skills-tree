---
name: table-extraction
description: Extract tables from documents, images, and web content into structured rows and columns while detecting merged cells, missing headers, and uncertain boundaries.
license: MIT
metadata:
  source: skills/01-perception/table-extraction.md
  version: "v2"
---

# Table Extraction

1. Identify whether the table is text-based, rendered, scanned, or DOM-based.
2. Extract headers, rows, merged cells, spans, and units.
3. Preserve the source page, region, or DOM location.
4. Distinguish empty cells from missing cells.
5. Validate column counts and data types after extraction.
6. Mark uncertain boundaries rather than silently shifting values between columns.

## Failure modes

- Merged cells: preserve row/column spans before flattening.
- Borderless tables: use alignment and repeated structure but mark low confidence.
- OCR errors: retain source coordinates and require verification for material values.

## Evidence

- https://docs.unstructured.io/open-source/core-functionality/partitioning
- https://camelot-py.readthedocs.io/
