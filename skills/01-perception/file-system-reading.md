---
title: "File System Reading"
category: 01-perception
level: basic
stability: stable
description: "Inspect files and directories with bounded traversal, explicit encoding handling, metadata capture, and path-safety checks."
related: [text-reading, structured-data-reading, json-schema-validation]
added: "2025-03"
version: v2
updated: "2026-09"
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-01-perception-file-system-reading.json)

# File System Reading

## Description

Inspect files and directories with bounded traversal, explicit encoding handling, metadata capture, and path-safety checks.

## When to Use

Use when an agent needs to discover or read local files while preventing accidental traversal outside an approved root.

## Inputs / Outputs

| Field | Type | Description |
|---|---|---|
| input | structured | Source content plus any format-specific metadata. |
| options | object | Limits, locale, schema, or provider-specific parsing options. |
| output | structured | Normalized records with provenance and explicit uncertainty. |

## Runnable Example

```python
from pathlib import Path

def read_text_under(root: Path, relative: str, max_bytes: int = 1_000_000) -> str:
    base = root.resolve()
    target = (base / relative).resolve()
    if target != base and base not in target.parents:
        raise PermissionError("path escapes approved root")
    if not target.is_file():
        raise FileNotFoundError(target)
    if target.stat().st_size > max_bytes:
        raise ValueError("file exceeds read limit")
    return target.read_text(encoding="utf-8")

root = Path(".")
print(read_text_under(root, "README.md")[:80])
```

## Failure Modes

| Failure | Cause | Mitigation |
|---|---|---|
| Path traversal | malformed or adversarial input | Validate structure before semantic processing. |
| symlink escapes | unexpected source variation | Preserve raw context and emit a warning. |
| huge files | incomplete source | Mark uncertainty instead of inventing values. |
| Resource exhaustion | unbounded input | Enforce size, time, and result limits. |

## Output Contract

File contents plus bounded metadata; reject unsafe paths and preserve the distinction between missing, inaccessible, and unreadable files.

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
