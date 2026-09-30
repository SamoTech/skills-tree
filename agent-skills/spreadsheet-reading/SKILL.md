---
name: spreadsheet-reading
description: Read XLSX, CSV, and ODS workbooks into bounded structured data while preserving sheet names, headers, formulas or cached values, and workbook metadata.
license: MIT
metadata:
  source: skills/01-perception/spreadsheet-reading.md
  version: "v2"
---

# Spreadsheet Reading

1. Detect the workbook format before selecting a parser.
2. Enumerate sheets before reading large workbooks.
3. Preserve headers, formulas, cached values, hidden-sheet state, and sheet names when relevant.
4. Bound rows, columns, file size, and total processing time.
5. Treat formulas and external links as data; never execute workbook macros as part of reading.
6. Report merged cells and ambiguous headers.

## Failure modes

- Formula values stale or absent: distinguish formula expressions from cached results.
- Merged headers: preserve the original structure before normalization.
- Malicious workbook content: parse without enabling macros or active content.

## Evidence

- https://pandas.pydata.org/docs/
- https://openpyxl.readthedocs.io/
- https://github.com/eea/odfpy

Evidence status: these references support implementation guidance; no performance benchmark is claimed without reproducible benchmark data.
