---
name: database-migration-writing
description: Write versioned, reversible schema migrations that ship application code and schema changes together, with explicit up and down paths, preflight checks, and lock-time budgeting.
metadata:
  source: skills/05-code/database-migration-writing.md
  category: 05-code
  version: "v1"
---

# Database Migration Writing

Category: Code | Level: intermediate | Stability: experimental | Version: v1

## Description

A schema migration is a deployment, not a script: it changes the shape every live query depends on while the system runs. This skill covers writing migrations that go additive-first, carry a real rollback path, preflight their base version, and order operations so hot tables are not locked longer than the change is worth.

## When to Use

Use for any change to a live database schema: new tables, columns, indexes, constraints, or type changes.

Do not mix one-off data surgery into a versioned migration; separate scripts keep both reviewable.

## Inputs

| Input | Type | Required | Description |
|---|---|---|---|
| `target_change` | `spec` | Yes | Desired schema delta, declaratively stated |
| `current_version` | `int` | Yes | Schema version the migration applies on top of |
| `engine` | `enum` | No | Dialect-specific lock and syntax rules |

## Procedure

1. State the change additively where possible: new nullable columns and new tables before renames, type changes, and drops.
2. Write the down migration and verify it actually reverses the up path on a copy, data included.
3. Preflight: assert the database's schema version equals `current_version`; refuse to run otherwise.
4. Order operations by lock cost: build indexes concurrently, backfill in batches, drop only after the code no longer reads the old shape.
5. Round-trip test up, down, up on a production-shaped copy.
6. Record the new version and the lock-time estimate in the migration's header.

## Outputs

| Output | Type | Description |
|---|---|---|
| `migration_files` | `list` | Versioned up/down files with preflight guards |
| `rollback_plan` | `object` | Steps and expected data state after down |
| `lock_estimate` | `object` | Expected blocking operations and durations |

## Runnable Example

```python
def order_operations(steps):
    additive = [s for s in steps if s["kind"] in ("create_table", "add_column", "add_index_concurrently")]
    rest = [s for s in steps if s not in additive]
    return additive + rest

steps = [
    {"name": "drop legacy_users", "kind": "drop_table"},
    {"name": "add users.region", "kind": "add_column"},
    {"name": "add users_region_idx", "kind": "add_index_concurrently"},
]
print([s["name"] for s in order_operations(steps)])
```

## Failure Modes

| Failure Mode | Cause | Mitigation |
|---|---|---|
| Destructive step before backfill | Column dropped or retyped while still read | Add new shape, migrate code, then drop |
| Down migration is a stub | Rollback written but never tested on data | Round-trip up/down/up on a copy |
| Long lock on a hot table | Blocking index build or type change | Concurrent builds, batched backfills |
| Version drift | Migration applied on an unexpected base | Preflight the schema version |
| Schema and data changes entangled | One migration does both | Split into schema migrations and data scripts |

## Security and Authority Boundary

Migrations execute with elevated database rights. Grant the minimum per step, never embed credentials or secrets in migration files, and treat down migrations with the same review standard as up migrations because they can destroy data.

## Evidence

This skill is grounded in dated public implementation references:

1. The Alembic database migration tool (https://pypi.org/project/alembic/).
2. The Flyway database migration project (https://github.com/flyway/flyway).

Honest boundary: these are implementation references, not adoption or demand evidence; this entry was added under the owner-directed corpus expansion recorded in `meta/memory/DECISIONS.md`, and no demand signal is claimed for it.

## Related Skills

- [DB Schema Design](db-schema-design.md) — the schema being migrated is designed here.
- [SQL Query Generation](sql-query-generation.md) — the query layer that must survive the migration.

## Changelog

| Date | Version | Change |
|---|---|---|
| `2026-10` | v1 | Initial entry added under the owner-directed corpus expansion |
