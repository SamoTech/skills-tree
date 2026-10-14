---
name: multi-tenant-memory-isolation
description: Scope agent memory reads and writes per tenant with isolation checks so one tenant cannot observe another tenant records.
metadata:
  source: skills/03-memory/multi-tenant-memory-isolation.md
  category: 03-memory
  version: "v1"
---
# Multi Tenant Memory Isolation

## Description
Scope agent memory reads and writes per tenant with isolation checks so one tenant cannot observe another tenant records. The procedure is constrained by explicit inputs and acceptance criteria rather than best-effort judgment alone.

## When to Use
- A task requires multi tenant memory isolation before downstream steps can proceed safely.
- Ambiguity or missing evidence would change the outcome.
- The result must be recorded with reasons and evidence for later verification.

## Inputs / Outputs
| Area | Contract |
|---|---|
| Inputs | Task context, candidate inputs, and explicit acceptance criteria for multi tenant memory isolation. |
| Outputs | A decision or artifact with recorded reasons, rejected alternatives, and verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Define the goal, the constraints, and the boundary of what this procedure may change.
2. Inventory the available inputs and flag gaps or ambiguities that block progress.
3. Execute the multi tenant memory isolation steps in a bounded, checkpointed way.
4. Compare the actual outcome against the expected outcome and record deviations.
5. On failure, apply the declared fallback path, and never widen permissions to recover.
6. Emit a structured result with evidence and provenance for downstream consumers.

## Runnable Example
```python
def visible(record, tenant):
    return record["tenant"] == tenant
assert visible({"tenant": "t1"}, "t1") is True
assert visible({"tenant": "t1"}, "t2") is False
```

## Failure Modes
- Acting outside the declared task boundary.
- Assuming an estimate or preview equals the verified effect.
- Retrying without preserving state or evidence.
- Using stale inputs as if they were current.
- Reporting success without checking the resulting state.

## Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result.

## Evidence
Multi-tenant agent deployments repeatedly request memory isolation guarantees in 2026 security threads. These are dated public signals, not adoption metrics.

## Related
- need-to-know-memory-scoping.md
- memory-access-auditing.md
- user-profile-memory.md
