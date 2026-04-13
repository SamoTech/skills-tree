![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-12-data-data-cleaning.json)

# Data Cleaning

**Category:** `data`  
**Skill Level:** `intermediate`  
**Stability:** `stable`
**Added:** 2025-03

### Description

Detect and fix data quality issues: remove nulls, deduplicate rows, fix data types, standardize formats, and handle outliers.

### Inputs

| Input | Type | Required | Description |
|---|---|---|---|
| `dataset` | `DataFrame/list` | ✅ | Raw dataset to clean |
| `rules` | `dict` | ❌ | Cleaning rules (drop nulls, cast types, etc.) |

### Outputs

| Output | Type | Description |
|---|---|---|
| `clean_dataset` | `DataFrame` | Cleaned dataset |
| `report` | `dict` | Summary of changes made |

### Example

```python
df = df.dropna(subset=['email'])
df = df.drop_duplicates()
df['date'] = pd.to_datetime(df['date'])
```

### Related Skills

- [CSV Processing](csv-processing.md)
- [Anomaly Detection](anomaly-detection.md)
- [Data Schema Inference](schema-inference.md)
