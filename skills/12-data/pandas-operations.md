![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-12-data-pandas-operations.json)

# Pandas Operations

**Category:** `data`  
**Skill Level:** `intermediate`  
**Stability:** `stable`
**Added:** 2025-03

### Description

Perform the full range of pandas DataFrame operations: slicing, indexing, apply, merge, reshape, window functions, and more.

### Example

```python
import pandas as pd
df['revenue_growth'] = df['revenue'].pct_change()
df['rolling_avg'] = df['revenue'].rolling(window=7).mean()
```

### Related Skills

- [CSV Processing](csv-processing.md)
- [Data Aggregation](data-aggregation.md)
- [Data Cleaning](data-cleaning.md)
