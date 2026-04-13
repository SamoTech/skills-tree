![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-12-data-data-filtering.json)

# Data Filtering

**Category:** `data`  
**Skill Level:** `basic`  
**Stability:** `stable`
**Added:** 2025-03

### Description

Filter datasets by one or more conditions to produce a relevant subset of rows or columns.

### Example

```python
# Pandas
df_filtered = df[(df['age'] > 18) & (df['country'] == 'EG')]

# SQL equivalent
# SELECT * FROM users WHERE age > 18 AND country = 'EG'
```

### Related Skills

- [Data Aggregation](data-aggregation.md)
- [SQL Query Execution](sql-execution.md)
