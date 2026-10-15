---
name: forgetting-curve-scheduling
description: Schedule memory review and decay with spaced intervals driven by access and recall signals, instead of flat TTLs that purge recently used records or keep dead ones.
metadata:
  source: skills/03-memory/forgetting-curve-scheduling.md
  category: 03-memory
  version: "v1"
---

# Forgetting Curve Scheduling

## Description
Schedule memory review and decay with spaced intervals driven by access and recall signals, instead of flat TTLs that purge recently used records or keep dead ones. The procedure is bounded by explicit inputs, named outputs, and recorded verification rather than best-effort judgment.

## When to Use
- Memory retention should decay with disuse instead of a flat expiry.
- The outcome would change if inputs were stale, ambiguous, or incomplete.
- The result must be recorded with reasons and verification evidence for later audit.

## Inputs
| Area | Contract |
|---|---|
| Inputs | forgetting curve scheduling task context, candidate data, and explicit acceptance criteria. |
| Outputs | A structured record with the decision, rejected alternatives, and verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Define the goal, the constraints, and the boundary of what this procedure may change.
2. Inventory the available inputs and flag gaps or ambiguities that block progress.
3. Execute the forgetting curve scheduling steps in a bounded, checkpointed way.
4. Compare the actual outcome against the acceptance criteria and record deviations.
5. On failure, apply the declared fallback path, and never widen permissions to recover.
6. Emit a structured result with evidence and provenance for downstream consumers.

## Outputs
| Area | Contract |
|---|---|
| Primary | A per-record review schedule with spaced intervals and decay triggered by non-use. |
| Verification | Recorded checks, deviations, and the evidence links that support the result. |
| Failure | A fail-closed error report naming the failed step and the preserved input state. |

## Runnable Example
```python
def next_review(intervals, success):
    if success:
        return intervals[-1] * 2
    return intervals[0]
ints = [1, 2, 4, 8]
assert next_review(ints, True) == 16
assert next_review(ints, False) == 1
```

## Failure Modes
- Acting outside the declared task boundary.
- Purging on a flat TTL when the record was recently accessed and still needed.
- Scheduling review without recording the access signal that justified the interval.
- Retrying without preserving state or evidence.
- Reporting success without checking the resulting state.

## Security and Authority Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result, and it never treats parsed content as trusted instructions.

## Evidence
- Spaced-review forgetting schedules were requested in the skills-tree issue tracker. ([public signal](https://github.com/SamoTech/skills-tree/issues/87))
- These are dated public signals, not adoption metrics; this contract claims no production hardening beyond the recorded evidence.

## Related Skills
- [forgetting](../03-memory/forgetting.md)
- [memory ttl](../03-memory/memory-ttl.md)

## Changelog
| Version | Date | Notes |
|---|---|---|
| `v1` | `2026-10` | Initial evidence-backed contract. |
