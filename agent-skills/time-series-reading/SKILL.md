---
name: time-series-reading
description: Load time-indexed data from files, databases, or APIs, normalize timestamps and sampling intervals, and produce analysis-ready series without hiding missing or irregular observations.
license: MIT
metadata:
  source: skills/01-perception/time-series-reading.md
  version: "v2"
---

# Time Series Reading

1. Identify the timestamp field, timezone, frequency, and units.
2. Parse timestamps with explicit timezone handling.
3. Detect duplicate, missing, out-of-order, and irregular observations.
4. Resample only when the analysis requires it and document the aggregation method.
5. Preserve raw observations when producing normalized series.
6. Do not interpolate missing data unless explicitly requested.

## Failure modes

- DST transitions: use timezone-aware timestamps and report ambiguous/nonexistent times.
- Irregular sampling: distinguish observed cadence from resampled cadence.
- Missing observations: preserve missingness rather than presenting interpolation as measured data.

## Evidence

- https://pandas.pydata.org/docs/user_guide/timeseries.html
- https://docs.pola.rs/
