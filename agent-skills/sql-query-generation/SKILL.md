---
name: sql-query-generation
description: Generate SQL from explicit data requirements, schema constraints, and supported database dialects while preserving correctness and safe parameter handling.
metadata:
  source: skills/05-code/sql-query-generation.md
  category: 05-code
  version: "v2"
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-05-code-sql-query-generation.json)

# SQL Query Generation

**Category:** `code`
**Skill Level:** `advanced`
**Stability:** `stable`
**Added:** 2026-09

### Description

Generate SQL from explicit data requirements, schema constraints, and supported database dialects while preserving correctness and safe parameter handling. The skill is evidence-first: inspect actual state before acting, preserve existing contracts, and verify the result before reporting completion.

### Inputs / Outputs

| Direction | Field | Type | Contract |
|---|---|---|---|
| Input | schema | object | Tables, columns, types, and constraints read from the actual database |
| Input | requirement | object | Result shape, filters, expected volume, and the target dialect |
| Output | sql | object | Parameterized, dialect-correct queries with explicit joins and filters |
| Output | verification | object | Explain-plan or test-database evidence including edge cases |

### Procedure
1. Read the actual schema (tables, columns, types, constraints) before writing the query.
2. Confirm the dialect and its syntax differences: quoting, functions, limit clauses.
3. Parameterize every external value; never interpolate untrusted input into SQL.
4. Make joins and filters explicit; avoid SELECT * in production paths.
5. Validate result shape and edge cases (empty sets, nulls, duplicates) against a test database or explain plan.
6. Record performance characteristics for large tables.

### Example

```python
query = 'SELECT id, name FROM users WHERE status = ?'
parameter = 'active'
assert '?' in query and parameter.isalpha()
print(query, '| parameter bound safely:', parameter)
```

### Related Skills

- [DB Schema Design](db-schema-design.md) - the schema the queries run against
- [Database Migration Writing](database-migration-writing.md) - versioned schema changes
- [Input Sanitization](../14-security/input-sanitization.md) - parameterize untrusted values

## Failure Modes

- Guessing table or column names instead of reading the schema.
- Interpolating untrusted values into SQL.
- Ignoring dialect differences.
- Skipping result-shape and edge-case validation.

## Changelog
- v2 (2026-11): Structural modernization; added the input/output contract table, a deterministic parameterization example, an execution procedure, and corpus-verified related links.
- v1 (2026-09): Initial entry.

## Evidence

- https://agentskills.io/specification

Evidence status: implementation guidance only; no benchmark claim is made without reproducible evidence.
