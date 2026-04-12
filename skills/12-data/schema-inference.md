# Data Schema Inference

**Category:** `data`  
**Skill Level:** `intermediate`  
**Stability:** `stable`
**Added:** 2025-03

### Description

Automatically detect and infer column types, constraints, and structure from a raw dataset.

### Example

```python
import pandas as pd
df = pd.read_csv('data.csv')
print(df.dtypes)
print(df.describe())
```

### Related Skills

- [Data Cleaning](data-cleaning.md)
- [CSV Processing](csv-processing.md)
