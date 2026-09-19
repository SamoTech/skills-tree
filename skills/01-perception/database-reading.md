---
title: "Database Reading"
category: 01-perception
level: intermediate
stability: stable
description: "Inspect database metadata and query results safely, preserving schema information, nullability, cardinality, provenance, and query limitations."
related: [text-reading, structured-data-reading, json-schema-validation]
added: "2025-03"
version: v2
updated: "2026-09"
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-01-perception-database-reading.json)

# Database Reading

## Description

Inspect database metadata and query results safely, preserving schema information, nullability, cardinality, provenance, and query limitations.

## When to Use

Use when an agent needs to understand relational or structured database state without mutating data.

## Inputs / Outputs

| Field | Type | Description |
|---|---|---|
| input | structured | Source content plus any format-specific metadata. |
| options | object | Limits, locale, schema, or provider-specific parsing options. |
| output | structured | Normalized records with provenance and explicit uncertainty. |

## Runnable Example

```python
def normalize_rows(columns: list[str], rows: list[tuple]) -> list[dict]:
    if any(len(row) != len(columns) for row in rows):
        raise ValueError("row/column cardinality mismatch")
    return [dict(zip(columns, row, strict=True)) for row in rows]

columns = ["id", "name"]
rows = [(1, "Ada"), (2, None)]
print(normalize_rows(columns, rows))
```

## Failure Modes

| Failure | Cause | Mitigation |
|---|---|---|
| Schema drift | malformed or adversarial input | Validate structure before semantic processing. |
| null handling | unexpected source variation | Preserve raw context and emit a warning. |
| permission errors | incomplete source | Mark uncertainty instead of inventing values. |
| Resource exhaustion | unbounded input | Enforce size, time, and result limits. |

## Output Contract

Typed/normalized rows plus schema and query metadata; never treat absence from a limited result set as proof of absence.

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
