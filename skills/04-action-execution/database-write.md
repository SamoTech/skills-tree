![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-04-action-execution-database-write.json)

# Database Write

**Category:** `action-execution`  
**Skill Level:** `intermediate`  
**Stability:** `stable`
**Added:** 2025-03

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
