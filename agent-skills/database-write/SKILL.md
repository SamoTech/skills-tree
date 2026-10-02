---
name: database-write
description: Persist structured data with transaction boundaries, parameterized queries, validation, and explicit rollback behavior.
metadata:
  source: skills/04-action-execution/database-write.md
  category: 04-action-execution
---

# Database Write

## Description

Write validated data to a database using parameterized statements and an explicit transaction boundary. The action must make rollback behavior and authorization assumptions visible.

## When to Use

- Creating or updating application records.
- Persisting validated agent-generated state.
- Applying a small transactional mutation.

## Inputs / outputs / failure modes

| Input | Output | Failure mode |
|---|---|---|
| Connection | Database transaction | Connection failure |
| Validated fields | Insert/update result | Constraint violation |
| Parameters | Safe query | Injection risk |
| Commit policy | Durable state | Partial mutation |

## Runnable example

```python
import sqlite3

with sqlite3.connect("example.db") as db:
    db.execute("CREATE TABLE IF NOT EXISTS items (name TEXT)")
    db.execute("INSERT INTO items(name) VALUES (?)", ("approved",))
    db.commit()
print("transaction committed")
```

## Failure modes

- Building SQL through string concatenation.
- Committing before validation is complete.
- Performing dependent writes without a transaction.
- Logging credentials or sensitive row contents.

## Related

- ../01-perception/database-reading.md
- ../14-security/input-sanitization.md
- assertion.md

## Evidence

- AI_CONSTITUTION.md
- AGENTS.md
- Repository security and validation workflows
