---
title: "Code Reading"
category: 01-perception
level: intermediate
stability: stable
description: "Read unfamiliar source code by reconstructing control flow, data flow, contracts, side effects, dependencies, and failure boundaries before proposing changes."
added: "2025-03"
version: v2
updated: "2026-09"
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-01-perception-code-reading.json)

# Code Reading

## Description

Read unfamiliar source code by reconstructing control flow, data flow, contracts, side effects, dependencies, and failure boundaries before proposing changes.

## When to Use

Use during repository onboarding, incident analysis, code review, reverse engineering, and maintenance of legacy systems.

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
class CodeReading:
    entry_points: list[str]
    dependencies: list[str]
    state_changes: list[str]
    risks: list[str]

def reading_checklist(source: str) -> CodeReading:
    lines = source.splitlines()
    entries = [ln.strip() for ln in lines if ln.strip().startswith(("def ", "class "))]
    imports = [ln.strip() for ln in lines if ln.strip().startswith(("import ", "from "))]
    mutations = [ln.strip() for ln in lines if "=" in ln and not ln.strip().startswith("#")]
    risks = [ln.strip() for ln in lines if any(x in ln.lower() for x in ("exec(", "eval(", "subprocess", "password"))]
    return CodeReading(entries, imports, mutations, risks)

print(reading_checklist("import os\ndef load():\n    password = os.getenv('PASSWORD')"))
```

## Failure Modes

| Failure | Cause | Mitigation |
|---|---|---|
| Missing runtime context | malformed or adversarial input | Validate structure before semantic processing. |
| dynamic dispatch | unexpected source variation | Preserve raw context and emit a warning. |
| generated code | incomplete source | Mark uncertainty instead of inventing values. |
| Resource exhaustion | unbounded input | Enforce size, time, and result limits. |

## Output Contract

A factual code map and explicit unknowns. Do not infer behavior that cannot be established from available source/configuration.

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
