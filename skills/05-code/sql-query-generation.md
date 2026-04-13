---
title: "SQL Query Generation"
category: 05-code
level: intermediate
stability: stable
description: "Apply sql query generation in AI agent workflows."
added: "2025-03"
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-05-code-sql-query-generation.json)

# SQL Query Generation

**Category:** `code`  
**Skill Level:** `intermediate`  
**Stability:** `stable`
**Added:** 2025-03

### Description

Translate natural language questions into valid SQL queries for relational databases.

### Example

```
Input: "Show me the top 5 customers by total order value this year"
Output:
  SELECT c.name, SUM(o.amount) as total
  FROM customers c
  JOIN orders o ON o.customer_id = c.id
  WHERE YEAR(o.created_at) = 2026
  GROUP BY c.id
  ORDER BY total DESC
  LIMIT 5;
```

### Frameworks

- Vanna.ai (text-to-SQL fine-tuning)
- LangChain `SQLDatabaseChain`
- Any LLM with schema context

### Related Skills

- [SQL Query Execution](../12-data/sql-execution.md)
- [Database Schema Design](db-schema-design.md)
