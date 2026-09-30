---
title: Sql Query Generation
category: 05-code
level: advanced
stability: stable
description: Generate SQL from explicit data requirements, schema constraints, and supported database dialects while preserving correctness and safe parameter handling.
added: "2026-09"
related: [05-code]
---

## Description
Generate SQL from explicit data requirements, schema constraints, and supported database dialects while preserving correctness and safe parameter handling. Inspect the actual schema and query conventions before writing queries.

## When to Use
Use when a task requires a query, migration query, reporting query, or database interaction.

## Inputs / outputs / failure modes

| Area | Guidance |
|---|---|
| Inputs | Schema, required result, dialect, parameters, and performance constraints. |
| Outputs | Validated SQL with safe parameter handling and evidence. |
| Failure modes | Wrong schema assumptions, injection-prone interpolation, incorrect joins, or inefficient queries. |

## Runnable Example

```python
query = 'SELECT id, name FROM users WHERE status = ?'
parameter = 'active'
print(query)
print('parameter:', parameter)
```

## Failure modes
- Guessing table or column names.
- Interpolating untrusted values into SQL.
- Ignoring dialect differences.
- Failing to test result shape and edge cases.

## Related
- 05-code
- AI_CONSTITUTION.md
- meta/AGENT_OPERATING_MODEL.md

## Evidence
Repository-backed implementation guidance grounded in repository governance and validation workflows; no external benchmark claim is made.
