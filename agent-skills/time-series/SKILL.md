---
name: time-series
description: Analyze or transform timestamped series with validated ordering, explicit frequency, honest windows, and forecast intervals.
metadata:
  source: skills/12-data/time-series.md
  category: 12-data
  version: "v2"
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-12-data-time-series.json)

# Time Series

**Category:** `data`
**Skill Level:** `advanced`
**Stability:** `stable`
**Added:** 2025-03

### Description

Analyze or transform timestamped series with validated ordering, explicit frequency, honest windows, and forecast intervals. The data step is contract-first: validate the input contract before transforming, and verify the output against explicit expectations rather than trusting the pipeline.

### Inputs / Outputs

| Direction | Field | Type | Contract |
|---|---|---|---|
| Input | series | list of object | Timestamped values with a declared frequency and gaps |
| Input | analysis_spec | object | Window, seasonality, and forecast or anomaly parameters |
| Output | analysis | object | Trend/seasonality decomposition or forecast with intervals |
| Output | quality_report | object | Gap counts, duplicate timestamps, and frequency check |

### Procedure
1. Validate the series first: sort by timestamp, detect gaps and duplicates.
2. Declare the frequency; resample explicitly if the data is irregular.
3. Decompose into trend, seasonality, and residual before forecasting.
4. Never fit on future data; use rolling or expanding windows honestly.
5. Report forecast intervals, not point forecasts alone.

### Example

```python
series = [('d1', 10), ('d2', 12), ('d3', 11), ('d4', 13), ('d5', 15)]
values = [v for _, v in series]
ma3 = [round(sum(values[i-3:i]) / 3, 4) for i in range(3, len(values) + 1)]
assert ma3 == [11.0, 12.0, 13.0]
assert len(series) == 5
print({'n': len(series), 'ma3': ma3})
```

### Related Skills

- [Statistical Analysis](statistical-analysis.md) - underlying inference methods
- [Anomaly Detection](anomaly-detection.md) - flag deviations from the expected pattern
- [Cohort Analysis](cohort-analysis.md) - track groups across periods

## Failure Modes

- Unsorted or duplicate timestamps silently distorting trend estimates.
- Seasonality ignored, turning seasonal spikes into false anomalies.
- Look-ahead leakage: forecasts fit on data that includes the future.
- Point forecasts published without intervals.

## Changelog
- v2 (2026-11): Structural modernization; added the input/output contract table, a skill-specific execution procedure, a deterministic example, and corpus-verified related links (replaced the unresolvable cross-category related references).
- v1 (2025-03): Initial entry.

## Evidence

- https://agentskills.io/specification

Evidence status: implementation guidance only; runtime behavior must be checked against the executing pipeline's documentation; no benchmark claim is made without reproducible evidence.
