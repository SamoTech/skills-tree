---
title: "Agent Memory Schema Design"
category: 03-memory
level: advanced
stability: experimental
description: "Design typed memory schemas with explicit fields, retention rules, and provenance slots before storage, and reject writes that do not conform to the declared schema."
added: "2026-10"
version: v1
related: [memory-indexing, hierarchical-memory-organization, memory-ttl]
tags: [memory, schema, governance]
---

# Agent Memory Schema Design

## Description
Design typed memory schemas with explicit fields, retention rules, and provenance slots before storage, and reject writes that do not conform to the declared schema. The procedure is constrained by explicit inputs and acceptance criteria rather than best-effort judgment alone.

## When to Use
- a memory store needs a declared schema before the first write before downstream steps can proceed safely.
- Ambiguity or missing evidence would change the outcome.
- The result must be recorded with reasons and evidence for later verification.

## Inputs / Outputs
| Area | Contract |
|---|---|
| Inputs | Task context, candidate inputs, and explicit acceptance criteria for agent memory schema design work. |
| Outputs | A decision or artifact with recorded reasons, rejected alternatives, and verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Define the goal, the constraints, and the boundary of what this procedure may change.
2. Inventory the available inputs and flag gaps or ambiguities that block progress.
3. Execute the agent memory schema design steps in a bounded, checkpointed way.
4. Compare the actual outcome against the expected outcome and record deviations.
5. On failure, apply the declared fallback path, and never widen permissions to recover.
6. Emit a structured result with evidence and provenance for downstream consumers.

## Runnable Example
```python
SCHEMA = {"fact", "source", "ts"}

def validate_write(record):
    missing = SCHEMA - set(record)
    extra = set(record) - SCHEMA
    if missing or extra:
        return False, (sorted(missing), sorted(extra))
    return True, None

assert validate_write({"fact": "a", "source": "u", "ts": 1})[0] is True
ok, err = validate_write({"fact": "a"})
assert ok is False and "source" in err[0]
```

## Failure Modes
- Storing free-form text with no typed fields.
- Changing the schema without a migration plan for old records.
- Omitting provenance slots that later audits need.
- Allowing silent field overloading.
- Retaining records past the declared retention rule.

## Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result.

## Evidence
Memory governance for agents is a recurring 2026 concern as long-term memory adoption grows in public coverage; this is a dated signal, not an adoption metric.

## Related
- memory-indexing.md
- hierarchical-memory-organization.md
- memory-ttl.md
