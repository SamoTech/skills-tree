# Database Reading

**Category:** `perception`  
**Skill Level:** `intermediate`  
**Stability:** `stable`
**Added:** 2025-03

### Description

Connect to a database and read rows, schemas, and metadata using SQL or ORM queries.

### Example

```python
import sqlite3
conn = sqlite3.connect('data.db')
cursor = conn.cursor()
cursor.execute('SELECT * FROM skills LIMIT 10')
rows = cursor.fetchall()
```

### Related Skills

- [SQL Query Generation](../05-code/sql-query-generation.md)
- [Structured Data Reading](structured-data-reading.md)
