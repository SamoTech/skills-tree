![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-12-data-time-series.json)

# Time Series Analysis

**Category:** `data`  
**Skill Level:** `advanced`  
**Stability:** `stable`
**Added:** 2025-03

### Description

Analyze time-indexed data to identify trends, seasonality, anomalies, and produce forecasts.

### Example

```python
from prophet import Prophet
model = Prophet()
model.fit(df)  # df must have 'ds' (date) and 'y' (value) columns
forecast = model.predict(future)
```

### Frameworks

- Python `prophet`, `statsmodels`, `sktime`
- Pandas `resample()`, `rolling()`

### Related Skills

- [Statistical Analysis](statistical-analysis.md)
- [Anomaly Detection](anomaly-detection.md)
- [Data Visualization](data-visualization.md)
