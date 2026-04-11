# SQL Query Execution

**Category:** `data`  
**Skill Level:** `intermediate`  
**Stability:** `stable`

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
