---
title: "API Response Parsing"
category: 01-perception
level: intermediate
stability: stable
added: "2025-03"
description: "Parse heterogeneous API responses into validated, normalized records while preserving error context, pagination metadata, and provider-specific fields."
related: [text-reading, structured-data-reading, json-schema-validation]
version: v2
updated: "2026-09"
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-01-perception-api-response-parsing.json)

# API Response Parsing

## Description

Parse heterogeneous API responses into validated, normalized records while preserving error context, pagination metadata, and provider-specific fields.

## When to Use

Use when an agent receives JSON or structured HTTP responses from third-party APIs and downstream logic needs a stable internal representation.

## Inputs / Outputs

| Field | Type | Description |
|---|---|---|
| input | structured | Source content plus any format-specific metadata. |
| options | object | Limits, locale, schema, or provider-specific parsing options. |
| output | structured | Normalized records with provenance and explicit uncertainty. |

## Runnable Example

```python
from dataclasses import dataclass
from typing import Any

@dataclass(frozen=True)
class ApiResult:
    data: list[dict[str, Any]]
    next_cursor: str | None
    warnings: list[str]

def parse_api_response(payload: dict[str, Any]) -> ApiResult:
    items = payload.get("items", payload.get("data", []))
    if not isinstance(items, list):
        raise ValueError("API response items must be a list")

    normalized: list[dict[str, Any]] = []
    warnings: list[str] = []
    for item in items:
        if not isinstance(item, dict):
            warnings.append("ignored non-object item")
            continue
        normalized.append(dict(item))

    paging = payload.get("pagination") or payload.get("meta") or {}
    cursor = paging.get("next_cursor") if isinstance(paging, dict) else None
    return ApiResult(normalized, cursor, warnings)

result = parse_api_response({
    "items": [{"id": "42", "name": "Ada"}],
    "pagination": {"next_cursor": "abc"},
})
print(result)
```

## Failure Modes

| Failure | Cause | Mitigation |
|---|---|---|
| Malformed envelopes | malformed or adversarial input | Validate structure before semantic processing. |
| type drift | unexpected source variation | Preserve raw context and emit a warning. |
| missing pagination fields | incomplete source | Mark uncertainty instead of inventing values. |
| Resource exhaustion | unbounded input | Enforce size, time, and result limits. |

## Output Contract

A normalized list of records, an optional continuation cursor, and non-fatal parsing warnings.

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
