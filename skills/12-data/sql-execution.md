---
title: "SQL Query Execution"
category: 12-data
level: intermediate
stability: stable
description: "Apply sql query execution in AI agent workflows."
added: "2025-03"
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-12-data-sql-execution.json)

# SQL Query Execution

**Category:** `data`  
**Skill Level:** `intermediate`  
**Stability:** `stable`
**Added:** 2025-03

### Description

Execute SQL queries against relational databases (PostgreSQL, MySQL, SQLite, etc.) and return results.

### Example

```python
import psycopg2
conn = psycopg2.connect(DATABASE_URL)
cur = conn.cursor()
cur.execute("SELECT user_id, SUM(amount) FROM orders GROUP BY user_id LIMIT 10")
rows = cur.fetchall()
```

### Frameworks

- LangChain `SQLDatabaseChain`
- OpenAI function calling + `sqlalchemy`
- Vanna.ai (text-to-SQL)

### Related Skills

- [SQL Query Generation](../05-code/sql-query-generation.md)
- [Data Aggregation](data-aggregation.md)
- [NoSQL Query](nosql-query.md)
