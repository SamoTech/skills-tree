# Anomaly Detection

**Category:** `data`  
**Skill Level:** `advanced`  
**Stability:** `stable`

### Description

Detect outliers and anomalies in datasets using statistical methods, isolation forests, or LLM-assisted analysis.

### Example

```python
from sklearn.ensemble import IsolationForest
clf = IsolationForest(contamination=0.05)
df['anomaly'] = clf.fit_predict(df[['value']])
```

### Frameworks

- Python `scikit-learn` — IsolationForest, LOF
- Python `pyod` — anomaly detection library
- OpenAI Code Interpreter

### Related Skills

- [Statistical Analysis](statistical-analysis.md)
- [Time Series Analysis](time-series.md)
