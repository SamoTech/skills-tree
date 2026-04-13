![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-01-perception-spreadsheet-reading.json)

# Spreadsheet Reading
Category: perception | Level: basic | Stability: stable | Version: v1

## Description
Read XLSX, CSV, and ODS spreadsheets into DataFrames or dict structures, handling multi-sheet workbooks.

## Inputs
- `path`: file path
- `sheet`: sheet name or index (optional)
- `header_row`: int (default 0)

## Outputs
- `data`: list of dicts or pandas DataFrame
- `sheets`: list of sheet names

## Example
```python
import pandas as pd
xls = pd.ExcelFile("report.xlsx")
for sheet in xls.sheet_names:
    df = xls.parse(sheet)
    print(f"{sheet}: {df.shape}")
```

## Frameworks
| Framework | Method |
|---|---|
| Python | `pandas`, `openpyxl` |
| LlamaIndex | `PandasExcelReader` |
| LangChain | `UnstructuredExcelLoader` |

## Failure Modes
- Merged header cells create unnamed columns
- Hidden rows/columns included by default
- Dates read as float serial numbers in older XLSX

## Related
- `structured-data-reading.md` · `table-extraction.md`

## Changelog
- v1 (2026-04): Initial entry
