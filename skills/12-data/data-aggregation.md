# Data Aggregation

**Category:** `data`  
**Skill Level:** `intermediate`  
**Stability:** `stable`

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
