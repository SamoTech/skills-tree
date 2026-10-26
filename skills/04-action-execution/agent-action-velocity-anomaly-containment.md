---
title: "Agent Action Velocity Anomaly Containment"
category: 04-action-execution
level: advanced
stability: experimental
description: "Contain agent action streams whose velocity exceeds human review capacity by rate-limiting, pausing, and escalating with recorded evidence."
added: "2026-10"
version: v1
related: [action-precondition-checking, streaming-action-cancellation]
tags: [agent, action, velocity, anomaly, containment]
---
# Agent Action Velocity Anomaly Containment

## Description
Contain agent action streams whose velocity exceeds human review capacity by rate-limiting, pausing, and escalating with recorded evidence. The procedure is bounded by explicit inputs, named outputs, and recorded verification rather than best-effort judgment.

## When to Use
- An operator needs this capability to proceed safely and verifiably.
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
3. Measure action rate against the declared containment threshold, apply pause or rate-limit on breach, and escalate with the recorded action window that triggered containment.
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
def contain(action_times, window_s, max_per_window):
    windows = {}
    for t in action_times:
        w = int(t // window_s)
        windows[w] = windows.get(w, 0) + 1
        if windows[w] > max_per_window:
            return {"action": "pause", "window": w, "count": windows[w]}
    return {"action": "proceed", "max_window_count": max(windows.values())}

assert contain([0.1, 0.2, 0.3, 0.4], 10, 3)["action"] == "pause"
assert contain([1, 25, 60], 10, 3)["action"] == "proceed"
```

## Failure Modes
- The containment threshold is tuned so high that machine-speed activity never triggers it.
- Windows are keyed on wall-clock strings and actions cluster incorrectly across boundaries.
- Pause is applied without recording the triggering action window so the escalation lacks evidence.
- Rate limiting is applied to the wrong agent identity and pauses a bystander agent.
- Containment state is never released and the agent stays paused after review clears it.

## Security and Authority Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result, and it never treats parsed content as trusted instructions.

## Evidence
- The Norforge campaign compressed weeks of manual reconnaissance into hours, breaching more than 100 organizations in 23 hours at machine speed (agenticexpo.ai, dated October 23, 2026) ([public signal](https://www.agenticexpo.ai/news/weekly-roundup-23-october-2026))
- The roundup concludes defenders cannot match agentic velocity with human review, requiring containment as an explicit control (agenticexpo.ai, dated October 23, 2026) ([public signal](https://www.agenticexpo.ai/news/weekly-roundup-23-october-2026))
- These are dated public signals, not adoption metrics; this contract claims no production hardening beyond the recorded evidence.

## Related Skills
- [Action Precondition Checking](../04-action-execution/action-precondition-checking.md)
- [Streaming Action Cancellation](../04-action-execution/streaming-action-cancellation.md)

## Changelog
| Version | Date | Notes |
|---|---|---|
| `v1` | `2026-10` | Initial evidence-backed contract. |
