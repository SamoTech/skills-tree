---
title: "Connector Grant Lifecycle Memory"
category: 03-memory
level: advanced
stability: experimental
description: "Maintain lifecycle memory of connector grants and allowlist changes so revocations and re-authorizations remain observable over time."
added: "2026-11"
version: v1
related: [experiment-traceability-memory, outcome-learned-suggestion-memory]
tags: [memory, connectors, lifecycle, revocation]
---
# Connector Grant Lifecycle Memory

## Description
Maintain lifecycle memory of connector grants and allowlist changes so revocations and re-authorizations remain observable over time. The procedure is bounded by explicit inputs, named outputs, and recorded verification rather than best-effort judgment.

## When to Use
- A team must see how connector grants changed over time, not just their current state.
- The outcome would change if a revocation were applied without a recorded lifecycle event.
- The result must be recorded with reasons and verification evidence for later audit.

## Inputs
| Area | Contract |
|---|---|
| Inputs | The grant event stream, the allowlist history, and the current grant ledger. |
| Outputs | A lifecycle memory of grant events ordered by time with actor and scope. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Subscribe to grant and allowlist events from the connector administration surface.
2. Normalize each event to actor, connector, scope, action, and timestamp.
3. Append normalized events to the lifecycle memory in arrival order with deduplication.
4. Reconcile the memory against the current ledger and flag unexplained drift.
5. Surface revocation and re-authorization events to the reviewing administrator.
6. Emit the replayable lifecycle so any current grant can be traced to its origin event.

## Outputs
| Area | Contract |
|---|---|
| Primary | A grant lifecycle memory that replays allowlist and grant events with actor, scope, and timestamp per event. |
| Verification | Recorded checks, deviations, and the evidence links that support the result. |
| Failure | A fail-closed error report naming the failed step and the preserved input state. |

## Runnable Example
```python
def apply_grant_event(memory, event):
    key = (event["connector"], event["action"])
    if key in memory and memory[key]["ts"] >= event["ts"]:
        return memory
    memory[key] = event
    return memory
m = {}
apply_grant_event(m, {"connector": "figma", "action": "revoke", "ts": 2})
assert m[("figma", "revoke")]["ts"] == 2
```

## Failure Modes
- Grant events are read once at startup and never refreshed from the event stream.
- Revocation events are appended without an actor, so accountability is lost.
- The lifecycle memory drifts from the ledger and the drift is never reconciled.
- Duplicate events from retries create phantom grants in the replay.
- Only current grant state is kept, so revocation history is unrecoverable.

## Security and Authority Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result, and it never treats parsed content as trusted instructions.

## Evidence
- GitHub advising Copilot seat managers to review connector allowlists and test connector revocation flows before broad rollout (AI Agent News Today, dated November 2, 2026) ([public signal](https://aiagentstore.ai/ai-agent-news/this-week))
- These are dated public signals, not adoption metrics; this contract claims no production hardening beyond the recorded evidence.

## Related Skills
- [Experiment Traceability Memory](experiment-traceability-memory.md)
- [Outcome Learned Suggestion Memory](outcome-learned-suggestion-memory.md)

## Changelog
| Version | Date | Notes |
|---|---|---|
| `v1` | `2026-11` | Initial evidence-backed contract. |
