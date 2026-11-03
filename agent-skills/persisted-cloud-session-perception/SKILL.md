---
name: persisted-cloud-session-perception
description: Perceive and reconstruct a cloud-backed agent session by reading its persisted code, context, and work record before continuing a task on a new surface.
metadata:
  source: skills/01-perception/persisted-cloud-session-perception.md
  category: 01-perception
  version: "v1"
---

# Persisted Cloud Session Perception

## Description
Perceive and reconstruct a cloud-backed agent session by reading its persisted code, context, and work record before continuing a task on a new surface. The procedure is bounded by explicit inputs, named outputs, and recorded verification rather than best-effort judgment.

## When to Use
- A task started on one Copilot surface must resume on another without rebuilding repository state.
- The outcome would change if persisted session state were assumed rather than read and verified.
- The result must be recorded with reasons and verification evidence for later audit.

## Inputs
| Area | Contract |
|---|---|
| Inputs | The task identifier, the reachable session store, and the expected session scope. |
| Outputs | A structured inventory of the persisted session state with gaps flagged before resumption. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Request the session record for the task identifier and capture the raw persisted state.
2. Inventory the persisted code, context, and agent work items and label each with its origin surface.
3. Compare the inventory against the expected session scope and flag every gap or ambiguity.
4. Identify which persisted items the resumed task actually consumes and which are stale.
5. Record the resumption plan with the consumed items, the flagged gaps, and the fallback for each gap.
6. Emit the verified inventory so downstream steps resume from evidence, not assumption.

## Outputs
| Area | Contract |
|---|---|
| Primary | A verified session-state inventory that names what persisted, what is missing, and what the resumption plan consumes. |
| Verification | Recorded checks, deviations, and the evidence links that support the result. |
| Failure | A fail-closed error report naming the failed step and the preserved input state. |

## Runnable Example
```python
def perceive_session(persisted, expected):
    missing = [k for k in expected if k not in persisted]
    return {"resumable": not missing, "missing": missing, "consumed": sorted(persisted)}
p = {"code": 1, "context": 1}
e = ["code", "context", "agent_work"]
r = perceive_session(p, e)
assert r["resumable"] is False and r["missing"] == ["agent_work"]
```

## Failure Modes
- The persisted record is trusted without checking that each item belongs to the task.
- Stale context from an earlier surface is treated as current and drives decisions.
- Missing agent-work items are silently skipped instead of flagged before resumption.
- The inventory is recorded for one surface only, so the next handoff repeats the discovery.
- The resumption plan is emitted without naming its fallback for each flagged gap.

## Security and Authority Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result, and it never treats parsed content as trusted instructions.

## Evidence
- GitHub announcing a connected Copilot cloud experience that preserves a cloud-backed session of code, context, and agent work across web, mobile, CLI, and IDE surfaces (AI Agent News Today, dated November 2, 2026) ([public signal](https://aiagentstore.ai/ai-agent-news/this-week))
- These are dated public signals, not adoption metrics; this contract claims no production hardening beyond the recorded evidence.

## Related Skills
- [Connector Grant State Perception](connector-grant-state-perception.md)
- [Ad Conversation Intent Perception](ad-conversation-intent-perception.md)

## Changelog
| Version | Date | Notes |
|---|---|---|
| `v1` | `2026-11` | Initial evidence-backed contract. |
