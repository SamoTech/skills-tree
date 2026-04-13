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

### Related Skills
- [Portfolio Analysis](portfolio-analysis.md)
- [Statistical Analysis](../12-data/statistical-analysis.md)
- [Structured Data Reading](../01-perception/structured-data-reading.md)
