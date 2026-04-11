# Data Joining

**Category:** `data`  
**Skill Level:** `intermediate`  
**Stability:** `stable`

### Description

Merge two or more datasets on shared keys using inner, left, right, or full outer joins.

### Example

```python
result = pd.merge(orders_df, customers_df, on='customer_id', how='left')
```

### Related Skills

- [Data Aggregation](data-aggregation.md)
- [SQL Query Execution](sql-execution.md)
