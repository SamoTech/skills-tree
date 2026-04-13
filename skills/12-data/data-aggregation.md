---
title: "Data Aggregation"
category: 12-data
level: intermediate
stability: stable
description: "Apply data aggregation in AI agent workflows."
added: "2025-03"
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-12-data-data-aggregation.json)

# Data Aggregation

**Category:** `data`  
**Skill Level:** `intermediate`  
**Stability:** `stable`
**Added:** 2025-03

### Description

Group, sum, count, average, and pivot datasets to produce summary statistics and aggregated views.

### Example

```python
df.groupby('category')['revenue'].agg(['sum', 'mean', 'count'])
```

### Frameworks

- Python `pandas` — `groupby()`, `pivot_table()`
- SQL `GROUP BY`
- Apache Spark `groupBy()`

### Related Skills

- [Data Filtering](data-filtering.md)
- [Statistical Analysis](statistical-analysis.md)
- [SQL Query Execution](sql-execution.md)
