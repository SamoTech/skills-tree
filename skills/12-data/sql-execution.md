---
title: "Sql Execution"
category: 12-data
level: advanced
stability: stable
version: v2
description: "Execute bounded SQL with parameterized values, enforced access scope, explicit limits, and visible plan cost."
added: "2025-03"
related: [query-optimization, nosql-query, data-joining]
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-12-data-sql-execution.json)

# Sql Execution

**Category:** `data`
**Skill Level:** `advanced`
**Stability:** `stable`
**Added:** 2025-03

### Description

Execute bounded SQL with parameterized values, enforced access scope, explicit limits, and visible plan cost. The data step is contract-first: validate the input contract before transforming, and verify the output against explicit expectations rather than trusting the pipeline.

### Inputs / Outputs

| Direction | Field | Type | Contract |
|---|---|---|---|
| Input | statement | object | The SQL with declared parameters (no interpolated values) |
| Input | access_scope | object | Read-only vs write, row/time limits, and allowed tables |
| Output | rows | list of object | Result rows bounded by the declared limits |
| Output | execution_report | object | Rows returned, elapsed time, and the plan's scan type |

### Procedure
1. Classify the statement (read vs write) and enforce the access scope.
2. Parameterize every value; never interpolate inputs into SQL text.
3. Apply explicit row and time limits before executing.
4. Inspect the plan for full scans on large tables before running blind.
5. Report rows returned and the scan type so cost is visible.

### Example

```python
stmt = {'sql': 'SELECT id FROM orders WHERE status = :status LIMIT :lim', 'params': {'status': 'open', 'lim': 2}}
table = [{'id': 1, 'status': 'open'}, {'id': 2, 'status': 'done'}, {'id': 3, 'status': 'open'}]
def run(stmt, table):
    lim = stmt['params']['lim']
    return [r['id'] for r in table if r['status'] == stmt['params']['status']][:lim]
rows = run(stmt, table)
assert rows == [1, 3] and len(rows) <= stmt['params']['lim']
print({'rows': rows, 'parameterized': ':' in stmt['sql']})
```

### Related Skills

- [Query Optimization](query-optimization.md) - reduce the cost before running
- [Nosql Query](nosql-query.md) - document-store counterpart
- [Data Joining](data-joining.md) - combine tables correctly

## Failure Modes

- String-interpolated inputs enabling injection.
- Unbounded queries scanning whole tables without limits.
- Write statements run under a read-only scope by misclassification.
- No plan inspection, so a full scan on a huge table runs unseen.

## Changelog
- v2 (2026-11): Structural modernization; added the input/output contract table, a skill-specific execution procedure, a deterministic example, and corpus-verified related links (replaced the unresolvable cross-category related references).
- v1 (2025-03): Initial entry.

## Evidence

- https://agentskills.io/specification

Evidence status: implementation guidance only; runtime behavior must be checked against the executing pipeline's documentation; no benchmark claim is made without reproducible evidence.
