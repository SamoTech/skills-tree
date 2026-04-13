---
title: "Time Series Reading"
category: 01-perception
level: intermediate
stability: stable
description: "Apply time series reading in AI agent workflows."
added: "2025-03"
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-01-perception-time-series-reading.json)

# Time Series Reading
Category: perception | Level: intermediate | Stability: stable | Version: v1

## Description
Load and parse time-indexed data streams from files, databases, or APIs into analysis-ready structures.

## Inputs
- `source`: CSV, Parquet, InfluxDB, or API endpoint
- `timestamp_col`: column name
- `resample`: optional frequency string (e.g., `"1H"`)

## Outputs
- DatetimeIndex DataFrame with numeric columns

## Example
```python
import pandas as pd
df = pd.read_csv("metrics.csv", parse_dates=["timestamp"], index_col="timestamp")
df = df.resample("1H").mean().interpolate()
print(df.describe())
```

## Frameworks
| Framework | Method |
|---|---|
| Python | `pandas`, `polars` |
| TimescaleDB | SQL with `time_bucket()` |
| InfluxDB | Flux query language |

## Failure Modes
- Irregular sampling intervals cause resampling artifacts
- DST transitions create duplicate or missing timestamps

## Related
- `structured-data-reading.md` · `sensor-reading.md`

## Changelog
- v1 (2026-04): Initial entry
