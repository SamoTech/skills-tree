# SQL Tool

**Category:** `tool-use`  
**Skill Level:** `intermediate`  
**Stability:** `stable`

### Description

Expose SQL query execution as an agent tool, returning structured results from relational databases.

### Example

```python
import sqlite3

def run_sql(query: str, db_path: str = 'skills.db') -> list[dict]:
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute(query)
    return [dict(row) for row in cursor.fetchall()]
```

### Related Skills

- [SQL Query Generation](../05-code/sql-query-generation.md)
- [Database Reading](../01-perception/database-reading.md)
