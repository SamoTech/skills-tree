![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-12-data-nosql-query.json)

# NoSQL Query

**Category:** `data`  
**Skill Level:** `intermediate`  
**Stability:** `stable`
**Added:** 2025-03

### Description

Query document stores (MongoDB), key-value stores (Redis, DynamoDB), and wide-column stores (Cassandra).

### Example

```python
from pymongo import MongoClient
client = MongoClient(MONGO_URI)
db = client['mydb']
results = db.users.find({'age': {'$gt': 18}}, {'name': 1, 'email': 1})
```

### Related Skills

- [SQL Query Execution](sql-execution.md)
- [Vector DB Tool](../07-tool-use/vector-db-tool.md)
