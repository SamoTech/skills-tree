---
name: db-schema-design
description: Design database schemas from explicit data requirements, relationships, constraints, and access patterns.
metadata:
  source: skills/05-code/db-schema-design.md
  category: 05-code
  version: "v2"
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-05-code-db-schema-design.json)

# DB Schema Design

**Category:** `code`
**Skill Level:** `advanced`
**Stability:** `stable`
**Added:** 2026-09

### Description

Design database schemas from explicit data requirements, relationships, constraints, and access patterns. The skill is evidence-first: inspect actual state before acting, preserve existing contracts, and verify the result before reporting completion.

### Inputs / Outputs

| Direction | Field | Type | Contract |
|---|---|---|---|
| Input | requirements | object | Entities, relationships, cardinalities, constraints, and access patterns |
| Input | existing_schema | object | Current tables, migrations, indexes, and application queries |
| Output | schema | object | Tables, keys, constraints, and indexes derived from the requirements |
| Output | rationale | list of string | Normalization and index decisions with their justifications |

### Procedure
1. Inventory entities, relationships, and cardinalities from the explicit requirements.
2. Inspect the current schema, migrations, and the queries that will run against it.
3. Choose keys, constraints, and normalization; record every denormalization with its justification.
4. Design indexes from the stated access patterns, not from guesses.
5. Provide a forward migration path that preserves existing data.
6. Validate the design with the repository migration tooling before hand-off.

### Example

```python
from dataclasses import dataclass

@dataclass
class Field:
    name: str
    nullable: bool = False

fields = [Field('id'), Field('created_at'), Field('email', nullable=False)]
assert all(not f.nullable for f in fields if f.name == 'id')
print([f.name for f in fields])
```

### Related Skills

- [Database Migration Writing](database-migration-writing.md) - the versioned change path for the schema
- [SQL Query Generation](sql-query-generation.md) - the queries the schema must serve

## Failure Modes

- Designing without inspecting the current schema and live queries.
- Introducing destructive changes without a recovery path.
- Adding indexes unrelated to any stated access pattern.
- Claiming migration safety without executing validation.

## Changelog
- v2 (2026-11): Structural modernization; added the input/output contract table, a deterministic example, an execution procedure, and corpus-verified related links (removed the non-corpus AGENT_OPERATING_MODEL.md-style pointers).
- v1 (2026-09): Initial entry.

## Evidence

- https://agentskills.io/specification

Evidence status: implementation guidance only; no benchmark claim is made without reproducible evidence.
