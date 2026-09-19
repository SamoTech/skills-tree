---
title: "Chart Reading"
category: 01-perception
level: intermediate
stability: stable
description: "Interpret charts by separating visual extraction from semantic analysis, capturing axes, units, series, extrema, trends, and uncertainty before drawing conclusions."
added: "2025-03"
version: v2
updated: "2026-09"
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-01-perception-chart-reading.json)

# Chart Reading

## Description

Interpret charts by separating visual extraction from semantic analysis, capturing axes, units, series, extrema, trends, and uncertainty before drawing conclusions.

## When to Use

Use when an agent must answer questions about plotted data, dashboards, screenshots, or exported chart images.

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
class ChartObservation:
    title: str | None
    x_label: str | None
    y_label: str | None
    series: list[str]
    trend: str
    uncertainty: list[str]

def summarize_chart(obs: ChartObservation) -> str:
    series = ", ".join(obs.series) or "no identified series"
    uncertainty = "; ".join(obs.uncertainty) or "none recorded"
    return (
        f"Series: {series}. Trend: {obs.trend}. "
        f"Y axis: {obs.y_label or 'unknown'}. "
        f"Uncertainty: {uncertainty}."
    )

obs = ChartObservation("Revenue", "Month", "USD", ["Actual"], "rising", [])
print(summarize_chart(obs))
```

## Failure Modes

| Failure | Cause | Mitigation |
|---|---|---|
| Occluded labels | malformed or adversarial input | Validate structure before semantic processing. |
| dual axes | unexpected source variation | Preserve raw context and emit a warning. |
| misleading scales | incomplete source | Mark uncertainty instead of inventing values. |
| Resource exhaustion | unbounded input | Enforce size, time, and result limits. |

## Output Contract

A structured observation of chart metadata and visible trends, plus explicit uncertainty; not an invented dataset.

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
