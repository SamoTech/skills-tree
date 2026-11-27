---
title: "Data Summarization"
category: 12-data
level: advanced
stability: stable
version: v2
description: "Produce structured summaries with declared statistics, their bases, and the material assumptions that bound them."
added: "2025-03"
related: [data-aggregation, ab-test-analysis, funnel-analysis]
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-12-data-data-summarization.json)

# Data Summarization

**Category:** `data`
**Skill Level:** `advanced`
**Stability:** `stable`
**Added:** 2025-03

### Description

Produce structured summaries with declared statistics, their bases, and the material assumptions that bound them. The data step is contract-first: validate the input contract before transforming, and verify the output against explicit expectations rather than trusting the pipeline.

### Inputs / Outputs

| Direction | Field | Type | Contract |
|---|---|---|---|
| Input | dataset | list of object | Records with the measures to summarize |
| Input | summary_spec | object | Requested statistics, segments, and comparisons |
| Output | summary | object | Declared statistics with their bases (n, window, segment) |
| Output | caveats | list of string | Material assumptions and data limitations |

### Procedure
1. Declare which statistics are wanted and on which segment of the data.
2. Compute each statistic with its base (sample size, window) attached.
3. Prefer distributional summaries (min, median, max) over bare averages.
4. State material assumptions (coverage, period, exclusions) with the numbers.
5. Flag any statistic whose base is too small to be meaningful.

### Example

```python
xs = [4, 8, 15, 16, 23, 42]
xs_sorted = sorted(xs)
n = len(xs)
median = (xs_sorted[n//2 - 1] + xs_sorted[n//2]) / 2 if n % 2 == 0 else xs_sorted[n//2]
mean = sum(xs) / n
assert median == 15.5 and round(mean, 2) == 18.0 and n == 6
print({'n': n, 'median': median, 'mean': round(mean, 2)})
```

### Related Skills

- [Data Aggregation](data-aggregation.md) - build the aggregates to summarize
- [Ab Test Analysis](ab-test-analysis.md) - summarize experiment outcomes
- [Funnel Analysis](funnel-analysis.md) - summarize conversion stages

## Failure Modes

- Averages presented without sample size or distribution.
- Summaries computed over an undeclared subset of the data.
- Small-sample statistics reported as if representative.
- Assumptions and exclusions omitted from the summary.

## Changelog
- v2 (2026-11): Structural modernization; added the input/output contract table, a skill-specific execution procedure, a deterministic example, and corpus-verified related links (replaced the unresolvable cross-category related references).
- v1 (2025-03): Initial entry.

## Evidence

- https://agentskills.io/specification

Evidence status: implementation guidance only; runtime behavior must be checked against the executing pipeline's documentation; no benchmark claim is made without reproducible evidence.
