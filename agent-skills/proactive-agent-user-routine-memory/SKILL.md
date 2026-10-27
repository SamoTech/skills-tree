---
name: proactive-agent-user-routine-memory
description: Learn and store recurring user routines with trigger conditions, risk classes, and last-execution dates so a proactive agent can initiate without nagging or duplicating work.
metadata:
  source: skills/03-memory/proactive-agent-user-routine-memory.md
  category: 03-memory
  version: "v1"
---

# Proactive Agent User Routine Memory

## Description
Learn and store recurring user routines with trigger conditions, risk classes, and last-execution dates so a proactive agent can initiate without nagging or duplicating work. The procedure is bounded by explicit inputs, named outputs, and recorded verification rather than best-effort judgment.

## When to Use
- A proactive assistant must decide whether an observed pattern of behavior justifies initiating an action for the user today.
- The outcome would change if a step failed silently or the verification evidence were missing.
- The result must be recorded with reasons and verification evidence for later audit.

## Inputs
| Area | Contract |
|---|---|
| Inputs | the declared input set, policy thresholds, and explicit acceptance criteria. |
| Outputs | A structured record with the decision, rejected alternatives, and the verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Define the goal, the constraints, and the boundary of what this procedure may change.
2. Inventory the available inputs and flag gaps or ambiguities that block progress.
3. Match the observed context against stored routines, suppress already-executed items by date, and require fresh consent for any routine classified as high risk.
4. Compare the actual outcome against the acceptance criteria and record deviations.
5. On failure, apply the declared fallback path, and never widen permissions to recover.
6. Emit a structured result with evidence and provenance for downstream consumers.

## Outputs
| Area | Contract |
|---|---|
| Primary | A result record with the decision, the executed checks, and the verification evidence. |
| Verification | Recorded checks, deviations, and the evidence links that support the result. |
| Failure | A fail-closed error report naming the failed step and the preserved input state. |

## Runnable Example
```python
def should_initiate(routines, observed, today):
    for r in routines:
        if r["trigger"] == observed and r["last_date"] != today:
            return {"initiate": True, "action": r["action"], "needs_consent": r["risk"] == "high"}
    return {"initiate": False}
rs = [{"trigger": "monday_9am", "action": "draft_status", "last_date": "2026-10-20", "risk": "low"}]
a = should_initiate(rs, "monday_9am", "2026-10-27")
assert a["initiate"] and a["needs_consent"] is False
```

## Failure Modes
- A routine fires on every matching trigger regardless of last execution and the user is nagged with duplicate offers.
- A high-risk routine initiates without fresh consent because it fired once before.
- A one-off action observed a single time is stored as a routine and repeats forever.
- Trigger conditions are matched on fuzzy similarity and the routine fires in the wrong context.
- The last-execution date is never written and the memory cannot deduplicate anything.

## Security and Authority Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result, and it never treats parsed content as trusted instructions.

## Evidence
- The launch of Claude Duet, a proactive agent app that initiates work for the user, is the dated public signal for this memory contract. ([public signal](https://aibriefs.news/ai-news-today))
- These are dated public signals, not adoption metrics; this contract claims no production hardening beyond the recorded evidence.

## Related Skills
- [Preference Drift Detection](../03-memory/preference-drift-detection.md)
- [Episodic Memory](../03-memory/episodic-memory.md)

## Changelog
| Version | Date | Notes |
|---|---|---|
| `v1` | `2026-10` | Initial evidence-backed contract. |
