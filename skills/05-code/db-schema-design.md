---
title: Db Schema Design
category: 05-code
level: advanced
stability: stable
description: Design database schemas from explicit data requirements, relationships, constraints, and access patterns.
added: "2026-09"
related: [05-code]
---

## Description
Design database schemas from explicit data requirements, relationships, constraints, and access patterns. Inspect existing models, migrations, indexes, and application queries before changing a schema. Preserve compatibility and verify migrations.

## When to Use
Use when a task requires a new schema, a schema change, normalization decision, constraint, index, or migration plan.

## Inputs / outputs / failure modes

| Area | Guidance |
|---|---|
| Inputs | Requirements, existing schema, access patterns, migrations, and constraints. |
| Outputs | A justified schema or migration with verification evidence. |
| Failure modes | Data loss, incompatible migrations, missing constraints, or unsupported assumptions. |

## Runnable Example

```python
from dataclasses import dataclass

@dataclass
class Field:
    name: str
    nullable: bool = False

fields = [Field("id"), Field("created_at")]
print([f.name for f in fields])
```

## Failure modes
- Designing without inspecting the current schema.
- Introducing destructive changes without a recovery path.
- Ignoring query patterns and constraints.
- Claiming migration safety without executing validation.

## Related
- [AI Constitution](../../AI_CONSTITUTION.md)
- [Agent operating model](../../meta/AGENT_OPERATING_MODEL.md)

## Evidence
Repository-backed implementation guidance grounded in the repository governance and validation model; no external benchmark claim is made.
