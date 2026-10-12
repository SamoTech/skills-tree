---
name: financial-statement
description: Apply financial statement in an AI workflow with explicit scope, domain constraints, validation, and documented failure handling.
metadata:
  source: skills/16-domain-specific/financial-statement.md
  category: 16-domain-specific
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-16-domain-specific-financial-statement.json)

**Category:** Domain-Specific
**Skill Level:** `advanced`
**Stability:** stable
**Added:** 2026-04

### Description
Parses income statements, balance sheets, and cash flow statements to compute key financial ratios and performance metrics. Supports trend analysis, peer benchmarking, and narrative commentary generation for analyst or investor audiences.

### Example
```python
from dataclasses import dataclass

@dataclass
class FinancialRatios:
    gross_margin: float
    operating_margin: float
    current_ratio: float
    debt_to_equity: float

def analyse(revenue, cogs, opex, current_assets, current_liabilities, total_debt, equity):
    return FinancialRatios(
        gross_margin=round((revenue - cogs) / revenue, 4),
        operating_margin=round((revenue - cogs - opex) / revenue, 4),
        current_ratio=round(current_assets / current_liabilities, 2),
        debt_to_equity=round(total_debt / equity, 2),
    )

print(analyse(500_000, 200_000, 100_000, 120_000, 60_000, 80_000, 200_000))
```

## Failure Modes

- **Parsing misalignment:** period boundaries, units (thousands vs millions), or currency mismatches producing ratios that are arithmetically correct but economically wrong; re-verify scale and period before computing.
- **Ratio cherry-picking:** selecting metrics that support a preferred narrative; report the standard ratio set including unfavorable ones.
- **Trend distortion:** comparing periods affected by accounting-policy changes, restatements, or M&A without adjusting
or flagging them.
- **Benchmark incomparability:** peer sets with different fiscal calendars, scale, or business mix treated as comparable.
- **Narrative overreach:** commentary implying causation or forecasts from ratio movement alone; keep measured computation separate from interpretation.

## Evidence
The canonical skill file is the authoritative repository implementation. Repository schema, validation workflows, and the Agent Skills projection contract define structural conformance. Domain-specific factual claims must remain traceable to supplied or independently verified authoritative sources.

### Related
- 16-domain-specific
- input-guardrails
- output-guardrails
