---
name: csv-processing
description: Read, validate, and emit delimited records with declared formats, schemas, and reconciled row counts.
metadata:
  source: skills/12-data/csv-processing.md
  category: 12-data
  version: "v2"
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-12-data-csv-processing.json)

# Csv Processing

**Category:** `data`
**Skill Level:** `advanced`
**Stability:** `stable`
**Added:** 2025-03

### Description

Read, validate, and emit delimited records with declared formats, schemas, and reconciled row counts. The data step is contract-first: validate the input contract before transforming, and verify the output against explicit expectations rather than trusting the pipeline.

### Inputs / Outputs

| Direction | Field | Type | Contract |
|---|---|---|---|
| Input | source | object | Raw CSV bytes with declared delimiter, encoding, and header row |
| Input | schema | object | Expected columns, types, and nullability |
| Output | records | list of object | Parsed rows validated against the schema |
| Output | reject_report | list | Malformed rows with line numbers and reasons |

### Procedure
1. Confirm delimiter, encoding, and header presence before parsing anything.
2. Parse with a real CSV parser; never split raw text on commas manually.
3. Validate every row against the declared column schema (types, nullability).
4. Route malformed rows to a reject report with line numbers, not silent drops.
5. Report counts parsed, rejected, and emitted so totals reconcile.

### Example

```python
rows = [{'line': 1, 'cells': ['id', 'qty']}, {'line': 2, 'cells': ['a', '4']}, {'line': 3, 'cells': ['b', 'x']}]
def parse(cells):
    return {'id': cells[0], 'qty': int(cells[1])}
good, rejects = [], []
for r in rows[1:]:
    try:
        good.append(parse(r['cells']))
    except ValueError:
        rejects.append({'line': r['line']})
assert len(good) == 1 and good[0]['qty'] == 4 and rejects == [{'line': 3}]
print({'emitted': len(good), 'rejected': rejects})
```

### Related Skills

- [Data Cleaning](data-cleaning.md) - repair defective records
- [Schema Inference](schema-inference.md) - derive column types from data
- [Parquet Processing](parquet-processing.md) - columnar storage beyond CSV

## Failure Modes

- Quoted fields containing commas split by naive string splitting.
- Encoding mismatches (UTF-8 BOM, Latin-1) corrupting headers silently.
- Malformed rows dropped without a count, breaking row reconciliation.
- Type coercion errors surfacing downstream instead of at parse time.

## Changelog
- v2 (2026-11): Structural modernization; added the input/output contract table, a skill-specific execution procedure, a deterministic example, and corpus-verified related links (replaced the unresolvable cross-category related references).
- v1 (2025-03): Initial entry.

## Evidence

- https://agentskills.io/specification

Evidence status: implementation guidance only; runtime behavior must be checked against the executing pipeline's documentation; no benchmark claim is made without reproducible evidence.
