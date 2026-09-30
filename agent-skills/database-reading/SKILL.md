---
name: database-reading
description: Inspect database schemas and answer bounded read-only questions over retrieved rows while protecting user-controlled values. Use for schema-aware analytical agent workflows.
license: MIT
metadata:
  source: skills/01-perception/database-reading.md
  version: "v2"
---

# Database Reading

1. Inspect or receive the minimum schema required for the question.
2. Generate a read-only query constrained to the relevant tables and columns.
3. Parameterize all user-controlled values; never interpolate them into SQL.
4. Apply row, time, and cost limits.
5. Execute with a least-privilege read-only identity where possible.
6. Return the query, bounded result, and assumptions needed to reproduce the answer.

## Failure modes

- SQL injection: use parameter binding and reject arbitrary statement execution.
- Large scans: apply limits, filters, and query budgets.
- Sensitive data exposure: minimize selected columns and redact secrets or personal data.

## Evidence

- https://docs.python.org/3/library/sqlite3.html
- https://docs.python.org/3/library/sqlite3.html#how-to-use-placeholders-to-bind-values-in-sql-queries

Evidence status: these references support implementation guidance; no performance benchmark is claimed without reproducible benchmark data.
