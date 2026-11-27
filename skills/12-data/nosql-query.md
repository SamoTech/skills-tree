---
title: "Nosql Query"
category: 12-data
level: advanced
stability: stable
version: v2
description: "Construct and validate document-store queries with indexed filters, explicit projections, and consistency-aware reads."
added: "2025-03"
related: [sql-execution, query-optimization, schema-inference]
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-12-data-nosql-query.json)

# Nosql Query

**Category:** `data`
**Skill Level:** `advanced`
**Stability:** `stable`
**Added:** 2025-03

### Description

Construct and validate document-store queries with indexed filters, explicit projections, and consistency-aware reads. The data step is contract-first: validate the input contract before transforming, and verify the output against explicit expectations rather than trusting the pipeline.

### Inputs / Outputs

| Direction | Field | Type | Contract |
|---|---|---|---|
| Input | query_spec | object | The requested data with filters, projection, and limits |
| Input | store_profile | object | The store's indexing and consistency model |
| Output | results | list of object | Retrieved documents matching the declared filters |
| Output | query_report | object | Examined vs returned counts and index usage |

### Procedure
1. Translate the request into filters the store can serve with its indexes.
2. Declare projection and limit up front; never fetch whole collections.
3. Prefer indexed field filters over client-side post-filtering.
4. Check the consistency model: a stale read may answer an old question.
5. Report examined vs returned counts to detect unindexed scans.

### Example

```python
docs = [{'id': 1, 'status': 'open', 'prio': 2}, {'id': 2, 'status': 'done', 'prio': 1}, {'id': 3, 'status': 'open', 'prio': 5}]
indexed = {'status'}
filt = {'status': 'open'}
assert all(k in indexed for k in filt), 'unindexed filter'
results = [d for d in docs if all(d.get(k) == v for k, v in filt.items())]
assert len(results) == 2 and all(d['status'] == 'open' for d in results)
print({'matched': len(results), 'examined': len(docs), 'indexed': True})
```

### Related Skills

- [Sql Execution](sql-execution.md) - relational counterpart with the same discipline
- [Query Optimization](query-optimization.md) - reduce scan cost
- [Schema Inference](schema-inference.md) - confirm document field shapes

## Failure Modes

- Unindexed filter fields forcing full collection scans.
- Missing limits or projections pulling entire collections into memory.
- Eventual-consistency reads presented as current state.
- Client-side post-filtering mistaken for server-side query results.

## Changelog
- v2 (2026-11): Structural modernization; added the input/output contract table, a skill-specific execution procedure, a deterministic example, and corpus-verified related links (replaced the unresolvable cross-category related references).
- v1 (2025-03): Initial entry.

## Evidence

- https://agentskills.io/specification

Evidence status: implementation guidance only; runtime behavior must be checked against the executing pipeline's documentation; no benchmark claim is made without reproducible evidence.
