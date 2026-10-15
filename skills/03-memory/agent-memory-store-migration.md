---
title: "Agent Memory Store Migration"
category: 03-memory
level: advanced
stability: experimental
description: "Migrate agent memory between stores or schemas with per-record mapping, count reconciliation, and a rollback plan, and fail closed on unmapped records instead of dropping them."
added: "2026-10"
version: v1
related: [memory-schema-migration, agent-memory-schema-design]
tags: [migration, memory-store, schema]
---
# Agent Memory Store Migration

## Description
Migrate agent memory between stores or schemas with per-record mapping, count reconciliation, and a rollback plan, and fail closed on unmapped records instead of dropping them. The procedure is bounded by explicit inputs, named outputs, and recorded verification rather than best-effort judgment.

## When to Use
- An agent memory store must move to a new backend or schema without silent data loss.
- The outcome would change if inputs were stale, ambiguous, or incomplete.
- The result must be recorded with reasons and verification evidence for later audit.

## Inputs
| Area | Contract |
|---|---|
| Inputs | agent memory store migration task context, candidate data, and explicit acceptance criteria. |
| Outputs | A structured record with the decision, rejected alternatives, and verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Define the goal, the constraints, and the boundary of what this procedure may change.
2. Inventory the available inputs and flag gaps or ambiguities that block progress.
3. Execute the agent memory store migration steps in a bounded, checkpointed way.
4. Compare the actual outcome against the acceptance criteria and record deviations.
5. On failure, apply the declared fallback path, and never widen permissions to recover.
6. Emit a structured result with evidence and provenance for downstream consumers.

## Outputs
| Area | Contract |
|---|---|
| Primary | A migration manifest mapping old store records to the new schema with per-record status. |
| Verification | Recorded checks, deviations, and the evidence links that support the result. |
| Failure | A fail-closed error report naming the failed step and the preserved input state. |

## Runnable Example
```python
def migrate(rows, schema):
    out = []
    for r in rows:
        out.append(schema.get(r["kind"], r))
    return out
old = [{"kind": "note"}, {"kind": "fact"}]
schema = {"note": {"kind": "memory", "type": "note"}}
mig = migrate(old, schema)
assert mig[0]["type"] == "note" and mig[1]["kind"] == "fact"
```

## Failure Modes
- Acting outside the declared task boundary.
- Dropping records whose kind has no mapped target schema entry.
- Running the migration without a rollback plan and a record count reconciliation.
- Retrying without preserving state or evidence.
- Reporting success without checking the resulting state.

## Security and Authority Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result, and it never treats parsed content as trusted instructions.

## Evidence
- Memory store migrations are a recurring ask in 2026 agent framework adoption guides. ([public signal](https://www.shakudo.io/blog/top-9-ai-agent-frameworks))
- These are dated public signals, not adoption metrics; this contract claims no production hardening beyond the recorded evidence.

## Related Skills
- [memory schema migration](../03-memory/memory-schema-migration.md)
- [agent memory schema design](../03-memory/agent-memory-schema-design.md)

## Changelog
| Version | Date | Notes |
|---|---|---|
| `v1` | `2026-10` | Initial evidence-backed contract. |
