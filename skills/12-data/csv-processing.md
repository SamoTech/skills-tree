---
title: "CSV Processing"
category: 12-data
level: beginner
stability: stable
added: "2025-03"
description: "Apply CSV processing in AI agent workflows."
dependencies:
  - package: pandas
    min_version: "2.0.0"
    tested_version: "3.0.2"
    confidence: verified
code_blocks:
  - id: "example-csv"
    type: executable
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-12-data-csv-processing.json)

# CSV Processing

**Category:** `data`  
**Skill Level:** `beginner`  
**Stability:** `stable`
**Added:** 2025-03

### Description

Load, filter, transform, and export CSV data using pandas for structured analysis in agent pipelines.

### Example

```python
# pip install pandas
import pandas as pd
from io import StringIO

# Load
df = pd.read_csv("data.csv")

# Inspect
print(df.head())
print(df.dtypes)
print(df.describe())

# Filter
high_value = df[df["revenue"] > 10000]

# Transform
df["profit_margin"] = (df["profit"] / df["revenue"] * 100).round(2)

# Aggregate
by_region = df.groupby("region")["revenue"].sum().reset_index()

# Export
by_region.to_csv("output.csv", index=False)
```

### Related Skills
- `pandas-operations`, `schema-inference`, `data-visualization`, `sql-execution`
