---
title: "Contract Reading"
category: 01-perception
level: intermediate
stability: stable
description: "Extract obligations, definitions, dates, exceptions, parties, and risk-bearing clauses from contracts without collapsing legal language into unsupported conclusions."
related: [text-reading, structured-data-reading, json-schema-validation]
added: "2025-03"
version: v2
updated: "2026-09"
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-01-perception-contract-reading.json)

# Contract Reading

## Description

Extract obligations, definitions, dates, exceptions, parties, and risk-bearing clauses from contracts without collapsing legal language into unsupported conclusions.

## When to Use

Use for contract triage, clause extraction, obligation tracking, and preparation for human legal review.

## Inputs / Outputs

| Field | Type | Description |
|---|---|---|
| input | structured | Source content plus any format-specific metadata. |
| options | object | Limits, locale, schema, or provider-specific parsing options. |
| output | structured | Normalized records with provenance and explicit uncertainty. |

## Runnable Example

```python
import re

def extract_contract_signals(text: str) -> dict[str, list[str]]:
    sections = {"obligations": [], "deadlines": [], "exceptions": []}
    for line in text.splitlines():
        s = line.strip()
        if re.search(r"\bshall\b|\bmust\b", s, re.I):
            sections["obligations"].append(s)
        if re.search(r"\bwithin\s+\d+\s+days?\b|\bdeadline\b", s, re.I):
            sections["deadlines"].append(s)
        if re.search(r"\bexcept\b|\bunless\b|\bprovided that\b", s, re.I):
            sections["exceptions"].append(s)
    return sections

print(extract_contract_signals("Supplier shall deliver within 30 days unless force majeure applies."))
```

## Failure Modes

| Failure | Cause | Mitigation |
|---|---|---|
| Definitions outside the excerpt | malformed or adversarial input | Validate structure before semantic processing. |
| cross-references | unexpected source variation | Preserve raw context and emit a warning. |
| jurisdiction-specific meaning | incomplete source | Mark uncertainty instead of inventing values. |
| Resource exhaustion | unbounded input | Enforce size, time, and result limits. |

## Output Contract

Quoted or location-linked clause observations grouped by obligation, deadline, and exception; legal conclusions require qualified review.

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
