---
title: "Anomaly Detection"
category: 12-data
level: intermediate
stability: stable
added: "2025-03"
description: "Apply anomaly detection in AI agent workflows."
dependencies:
  - package: scikit-learn
    min_version: "1.3.0"
    tested_version: "1.8.0"
    confidence: verified
  - package: pandas
    min_version: "2.0.0"
    tested_version: "3.0.2"
    confidence: verified
code_blocks:
  - id: "example-anomaly"
    type: executable
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-12-data-anomaly-detection.json)

# Anomaly Detection

**Category:** `data`  
**Skill Level:** `intermediate`  
**Stability:** `stable`
**Added:** 2025-03

### Description

Detect statistical outliers and anomalous patterns in numerical datasets using Isolation Forest, Z-score, or LOF algorithms.

### Example

```python
# pip install scikit-learn pandas
import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler

df = pd.read_csv("metrics.csv")
features = df[["cpu_usage", "memory_mb", "latency_ms"]]

scaler = StandardScaler()
X_scaled = scaler.fit_transform(features)

iso = IsolationForest(contamination=0.05, random_state=42)
df["anomaly"] = iso.fit_predict(X_scaled)  # -1 = anomaly, 1 = normal

anomalies = df[df["anomaly"] == -1]
print(f"Detected {len(anomalies)} anomalies out of {len(df)} records")
print(anomalies.head())
```

### Related Skills
- `statistical-analysis`, `time-series`, `data-visualization`, `csv-processing`
