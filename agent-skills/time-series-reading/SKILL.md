---
name: time-series-reading
description: Load time-indexed data from files, databases, or APIs, normalize timestamps and sampling intervals, and produce analysis-ready series without hiding missing or irregular observations.
metadata:
  source: skills/01-perception/time-series-reading.md
  category: 01-perception
  version: "v3"
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-01-perception-time-series-reading.json)

# Time Series Reading

## Description
Load and parse time-indexed data from files, databases, or APIs into analysis-ready structures while normalizing timestamps and sampling intervals and preserving evidence of missing or irregular observations.

## When to Use
- Preparing metrics or sensor data for forecasting, anomaly detection, or reporting
- Normalizing irregular or mixed-frequency series before aggregation
- Auditable ingestion where gaps and resampling artifacts must remain visible

## Inputs / Outputs

| Direction | Field | Type | Contract |
|---|---|---|---|
| Input | `source` | CSV, Parquet, database, or API endpoint | Time-indexed source; the connector must state its timestamp precision |
| Input | `timestamp_col` | string | Column to parse as the index; timezone must be explicit or documented |
| Input | `resample` | optional frequency string | Target interval such as `"1H"`; aggregation function must be stated |
| Output | `series` | DatetimeIndex DataFrame | Numeric columns indexed by normalized timestamps |
| Output | `gaps` | list of intervals | Ranges with no observations; interpolation is recorded, never silent |
| Output | `sampling_report` | summary | Observed interval distribution and any DST or timezone anomalies |

## Example
```python
# pip install pandas
import pandas as pd

def load_series(path: str, ts_col: str = "timestamp", freq: str = "1H") -> tuple[pd.DataFrame, pd.Series]:
    df = pd.read_csv(path, parse_dates=[ts_col], index_col=ts_col)
    df = df.sort_index()
    expected = pd.date_range(df.index.min(), df.index.max(), freq=freq)
    gaps = expected.difference(df.index)
    filled = df.resample(freq).mean().interpolate()
    return filled, gaps

filled, gaps = load_series("metrics.csv")
print(filled.describe())
print("missing intervals:", len(gaps))
```

## Frameworks
| Framework | Method |
|---|---|
| Python | `pandas`, `polars` |
| TimescaleDB | SQL with `time_bucket()` |
| InfluxDB | Flux query language |

## Procedure
1. Confirm the source schema, timestamp precision, and timezone before parsing.
2. Parse timestamps explicitly; reject ambiguous local times or record the assumed timezone.
3. Sort by time and detect duplicate or missing intervals; emit them as a gaps report.
4. Resample only at the documented interval with a stated aggregation function.
5. Mark interpolated values so downstream consumers can distinguish observations from estimates.
6. Return the series with the sampling report attached.

## Failure Modes
- Irregular sampling intervals cause resampling artifacts: report the observed interval distribution instead of assuming regularity.
- DST transitions create duplicate or missing timestamps: normalize to UTC or document the zone before indexing.
- Interpolation fabricates plausible-looking data: mark interpolated points and exclude them from downstream verification counts.
- Mixed timezones across sources silently shift series: normalize first and record each source's original zone.
- Silent truncation of high-frequency data: bound and report the loaded window rather than dropping tails.

## Related
- [Structured Data Reading](structured-data-reading.md)
- [Sensor Reading](sensor-reading.md)

## Changelog
- v3 (2026-11): Structural modernization; added the input/output contract table, procedure, gap-handling failure modes, and removed the stale body metadata line that contradicted frontmatter.
- v1 (2026-04): Initial entry.

## Evidence

- https://pandas.pydata.org/docs/user_guide/timeseries.html
- https://docs.pola.rs/

Evidence status: these references support implementation guidance; no performance benchmark is claimed without reproducible benchmark data.
