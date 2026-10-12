---
name: energy-consumption-forecasting
description: Forecast electricity or gas demand over short and medium horizons using calendar effects, weather covariates, and load history, with error bands and explicit regime awareness.
metadata:
  source: skills/16-domain-specific/energy-consumption-forecasting.md
  category: 16-domain-specific
  version: "v1"
---

# Energy Consumption Forecasting

Category: Domain-Specific | Level: intermediate | Stability: experimental | Version: v1

## Description

Load forecasting is regular until it is not. The skill covers building the baseline from calendar and weather effects, adding autoregressive load structure, handling regime changes such as holidays and extreme events, and reporting forecasts with error bands calibrated on backtests rather than assumed. The deliverable is honest: a point forecast, an interval, and the conditions under which the forecast should be distrusted.

## When to Use

Use when operations or budgeting need expected demand: day-ahead scheduling, capacity planning, or billing projections.

Do not backtest on the same period used to tune the model. Self-graded forecasts always pass and then fail in production.

## Inputs

| Input | Type | Required | Description |
|---|---|---|---|
| `load_history` | `table` | Yes | Timestamped consumption series for the target meter or region |
| `weather_forecast` | `table` | Yes | Temperature and related covariates for the forecast horizon |
| `calendar` | `table` | Yes | Holidays, weekends, and special-day flags for the horizon |

## Procedure

1. Clean the load history: gaps, daylight-saving transitions, and meter rollovers handled explicitly.
2. Engineer calendar and weather features: hour, weekday, holiday, heating and cooling degrees.
3. Fit the baseline and autoregressive components on training data only.
4. Backtest on held-out recent periods and calibrate error bands from realized residuals.
5. Adjust for regime days, such as holidays and extreme weather, with dedicated handling.
6. Publish the forecast with intervals and the regime assumptions it depends on.

## Outputs

| Output | Type | Description |
|---|---|---|
| `forecast` | `table` | Expected demand per interval in the horizon |
| `error_bands` | `table` | Calibrated prediction intervals per interval |
| `regime_notes` | `list` | Regime assumptions and their effect on the forecast |

## Runnable Example

```python
def weather_adjust(base_load, temp, bands):
    """bands: {range: multiplier}"""
    for (lo, hi), mult in bands.items():
        if lo <= temp < hi:
            return round(base_load * mult, 2)
    return round(base_load, 2)

print(weather_adjust(100.0, 2.0, {(0, 15): 1.3, (15, 22): 1.0, (22, 40): 1.5}))
print(weather_adjust(100.0, 25.0, {(0, 15): 1.3, (15, 22): 1.0, (22, 40): 1.5}))
```

## Failure Modes

| Failure Mode | Cause | Mitigation |
|---|---|---|
| Self-graded accuracy | Backtests on the tuning window | Hold out recent periods before judging accuracy |
| DST double-counted | Repeated or skipped hours corrupt features | Normalize timestamps to one clock before features |
| Holiday regime ignored | Special days forecast as ordinary weekdays | Dedicated handling for known regime days |
| Weather source mismatch | Forecast covariates from a different station | Use the same covariate source in training and serving |
| Point forecasts only | No intervals, no stated assumptions | Publish calibrated bands and regime notes |

## Security and Authority Boundary

Consumption data reveals occupancy patterns and business activity. Aggregate or mask meter-level forecasts when shared beyond operations, and respect customer data agreements before joining consumption data with third-party sources.

## Evidence

This skill is grounded in dated public implementation references:

1. The Prophet forecasting library for seasonal time series (https://github.com/facebook/prophet).
2. The U.S. Energy Information Administration open energy statistics (https://www.eia.gov/).

Honest boundary: these are implementation references, not adoption or demand evidence; this entry was added under the owner-directed corpus expansion recorded in `meta/memory/DECISIONS.md`, and no demand signal is claimed for it.

## Related Skills

- [Time Series](time-series.md) — the temporal modeling layer the forecast builds on.
- [Statistical Analysis](statistical-analysis.md) — the backtesting discipline that calibrates the error bands.

## Changelog

| Date | Version | Change |
|---|---|---|
| `2026-10` | v1 | Initial entry added under the owner-directed corpus expansion |
