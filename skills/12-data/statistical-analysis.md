---
title: "Statistical Analysis"
category: 12-data
level: advanced
stability: stable
version: v2
description: "Apply declared statistical tests with checked assumptions, reported effect sizes, and stated limitations."
added: "2025-03"
related: [ab-test-analysis, cohort-analysis, time-series]
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-12-data-statistical-analysis.json)

# Statistical Analysis

**Category:** `data`
**Skill Level:** `advanced`
**Stability:** `stable`
**Added:** 2025-03

### Description

Apply declared statistical tests with checked assumptions, reported effect sizes, and stated limitations. The data step is contract-first: validate the input contract before transforming, and verify the output against explicit expectations rather than trusting the pipeline.

### Inputs / Outputs

| Direction | Field | Type | Contract |
|---|---|---|---|
| Input | sample | list of number | The observed values with their collection method |
| Input | analysis_spec | object | Declared test, significance level, and assumptions |
| Output | statistics | object | Descriptive statistics with sample size and spread |
| Output | inference | object | The test result with effect size and stated assumptions |

### Procedure
1. State the question and the declared test before computing anything.
2. Report descriptive statistics (n, mean, spread) before any inference.
3. Check the test's assumptions (normality, independence) or pick a robust alternative.
4. Report effect size with the p-value, never the p-value alone.
5. State the assumptions the conclusion depends on.

### Example

```python
xs = [2, 4, 4, 4, 5, 5, 7, 9]
n = len(xs)
mean = sum(xs) / n
var = sum((x - mean) ** 2 for x in xs) / (n - 1)
sd = var ** 0.5
assert n == 8 and round(mean, 4) == 5.0 and round(sd, 4) == 2.1381
print({'n': n, 'mean': mean, 'sd': round(sd, 4)})
```

### Related Skills

- [Ab Test Analysis](ab-test-analysis.md) - apply the discipline to experiments
- [Cohort Analysis](cohort-analysis.md) - compare groups over time
- [Time Series](time-series.md) - analyze temporally dependent data

## Failure Modes

- P-values reported without effect size or sample size.
- Assumption violations ignored because the test produced a number.
- Pseudoreplication: correlated samples treated as independent.
- Conclusions stated with confidence the design does not support.

## Changelog
- v2 (2026-11): Structural modernization; added the input/output contract table, a skill-specific execution procedure, a deterministic example, and corpus-verified related links (replaced the unresolvable cross-category related references).
- v1 (2025-03): Initial entry.

## Evidence

- https://agentskills.io/specification

Evidence status: implementation guidance only; runtime behavior must be checked against the executing pipeline's documentation; no benchmark claim is made without reproducible evidence.
