# Database Reading

**Category:** `perception`  
**Skill Level:** `intermediate`  
**Stability:** `stable`  
**Added:** 2025-03  
**Last Updated:** 2026-04

---

## Description

Read and interpret data from relational databases (PostgreSQL, MySQL, SQLite), NoSQL stores (MongoDB, DynamoDB), and time-series databases. The agent generates and executes queries, inspects schema structures, and converts raw rows into natural-language summaries or structured JSON. Supports schema introspection, sample-based profiling, and query explanation.

---

## Inputs

| Input | Type | Required | Description |
|---|---|---|---|
| `connection` | `object` | ✅ | DB connection object or DSN string |
| `question` | `string` | ✅ | Natural-language question about the data |
| `schema_hint` | `dict` | ❌ | Pre-fetched schema to skip introspection |

---

## Outputs

| Output | Type | Description |
|---|---|---|
| `sql` | `string` | Generated SQL query |
| `rows` | `list` | Raw result rows |
| `answer` | `string` | Natural-language answer to the question |

---

## Example

```python
import anthropic
import sqlite3
import json

client = anthropic.Anthropic()

def query_database_with_nl(db_path: str, question: str) -> str:
    """Answer a natural-language question against a SQLite database."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Introspect schema
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = [row[0] for row in cursor.fetchall()]
    schema = {}
    for table in tables:
        cursor.execute(f"PRAGMA table_info({table})")
        schema[table] = [row[1] for row in cursor.fetchall()]

    # Generate SQL via Claude
    sql_response = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=512,
        messages=[{
            "role": "user",
            "content": (
                f"Schema: {json.dumps(schema)}\n"
                f"Question: {question}\n"
                "Return ONLY a valid SQLite SELECT query, no explanation."
            )
        }]
    )
    sql = sql_response.content[0].text.strip().strip("```sql").strip("```").strip()

    # Execute and summarize
    cursor.execute(sql)
    rows = cursor.fetchmany(50)
    conn.close()

    summary = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=512,
        messages=[{
            "role": "user",
            "content": (
                f"Question: {question}\n"
                f"SQL: {sql}\n"
                f"Results ({len(rows)} rows): {rows}\n"
                "Answer concisely based on these results."
            )
        }]
    )
    return summary.content[0].text

answer = query_database_with_nl("sales.db", "Which product had the highest revenue last month?")
print(answer)
```

---

## Frameworks & Models

| Framework / Model | Implementation | Since |
|---|---|---|
| LangChain | `SQLDatabaseChain` / `create_sql_agent` | v0.1 |
| LangGraph | Tool node wrapping DB cursor | v0.1 |
| Claude claude-opus-4-5 | Direct text prompt with schema | 2024-06 |

---

## Notes

- Always parameterize any user-supplied values before executing generated SQL
- Limit result sets (`LIMIT 50`) to avoid flooding the context window
- For large schemas, send only relevant tables rather than the full schema
- Never expose database credentials in prompts

---

## Related Skills

- [Structured Data Reading](structured-data-reading.md) — CSV/JSON/YAML parsing
- [API Response Parsing](api-response-parsing.md) — for REST API data sources
- [Text Reading](text-reading.md) — general text extraction

---

## Changelog

| Date | Change |
|---|---|
| `2026-04` | Expanded from stub: full description, I/O table, NL-to-SQL example, security notes |
| `2025-03` | Initial stub entry |
