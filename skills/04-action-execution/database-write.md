# Database Write

**Category:** `action-execution`  
**Skill Level:** `intermediate`  
**Stability:** `stable`

### Description

Insert, update, or delete records in a database using SQL or ORM operations.

### Example

```python
import sqlite3
conn = sqlite3.connect('data.db')
cursor = conn.cursor()
cursor.execute(
    'INSERT INTO skills (name, category) VALUES (?, ?)',
    ('tree-of-thought', 'reasoning')
)
conn.commit()
conn.close()
```

### Related Skills

- [Database Reading](../01-perception/database-reading.md)
- [SQL Query Generation](../05-code/sql-query-generation.md)
