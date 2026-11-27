---
name: sql-tool
description: Execute bounded SQL through an authorized database tool using parameterized queries, least privilege, transaction boundaries, and result validation.
metadata:
  source: skills/07-tool-use/sql-tool.md
  category: 07-tool-use
  version: "v2"
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-07-tool-use-sql-tool.json)

# SQL Tool

**Category:** `tool-use`
**Skill Level:** `intermediate`
**Stability:** `stable`
**Added:** 2026-09

### Description

Execute bounded SQL through an authorized database tool using parameterized queries, least privilege, transaction boundaries, and result validation. The invocation is contract-first: least-privilege credentials, bounded scope, validated inputs, and post-action verification instead of trusting acknowledgements.

### Inputs / Outputs

| Direction | Field | Type | Contract |
|---|---|---|---|
| Input | query | object | Parameterized SQL with explicit parameters; no string interpolation |
| Input | scope | object | Target database, transaction boundary, and row/time limits |
| Output | result | object | Validated rows or mutation counts with the transaction outcome |
| Output | verification | object | Re-read or constraint check confirming the intended effect |

### Procedure
1. Use a role with the minimum privileges the operation needs; never write as an admin.
2. Parameterize every external value; reject any query that interpolates input into SQL text.
3. Bound the operation: LIMIT on reads, explicit transaction on multi-statement writes.
4. Validate result shape and edge cases (empty sets, nulls, duplicates) before use.
5. Verify mutations with a re-read inside the same transaction boundary where possible.
6. Record the executed statement, parameters, and affected-row counts as evidence.

### Example

```python
query = 'SELECT id, name FROM users WHERE status = ? LIMIT 100'
params = ['active']
assert '?' in query and 'LIMIT' in query
assert all(isinstance(p, str) for p in params)
print('parameterized, bounded query ready for execution')
```

### Related Skills

- [Tool Guardrails](tool-guardrails.md) - invocation boundaries and least privilege
- [Tool Output Validation](tool-output-validation.md) - validate provider responses before use
- [Input Sanitization](../14-security/input-sanitization.md) - reject interpolation of untrusted values

## Failure Modes

- Interpolating untrusted values into SQL text.
- Running with more privileges than the task needs.
- Unbounded reads or non-transactional multi-statement writes.
- Treating affected-rows counts as proof of business correctness.

## Changelog
- v2 (2026-11): Structural modernization; added the input/output contract table, a deterministic example, an execution procedure, and corpus-verified related links (replaced the non-corpus input-guardrails reference).
- v1 (2026-09): Initial entry.

## Evidence

- https://agentskills.io/specification
- https://www.postgresql.org/docs/current/sql.html

Evidence status: implementation guidance only; provider behavior must be checked against current provider documentation; no benchmark claim is made without reproducible evidence.
