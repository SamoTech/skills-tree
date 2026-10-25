---
title: "Watcher Driven Agent Ops Pattern"
category: 09-agentic-patterns
level: advanced
stability: experimental
description: "Wire observability watchers into a bounded agent operations loop so every watcher signal maps to a declared agent action or an explicit no-op."
added: "2026-10"
version: v1
related: [agent-fleet-monitoring, stuck-loop-detection]
tags: [watcher, driven, agent, ops, pattern]
---
# Watcher Driven Agent Ops Pattern

## Description
Wire observability watchers into a bounded agent operations loop so every watcher signal maps to a declared agent action or an explicit no-op. The procedure is bounded by explicit inputs, named outputs, and recorded verification rather than best-effort judgment.

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
3. Map each watcher signal class to exactly one declared response path, gate the response with a cost and blast-radius budget, and log unmatched signal classes as gaps instead of improvising.
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
def dispatch(signal, mapping, budget):
    path = mapping.get(signal["class"])
    if path is None:
        return {"action": "log-gap", "reason": "unmapped signal class"}
    if path["cost"] > budget["remaining"]:
        return {"action": "defer", "reason": "budget exceeded"}
    return {"action": path["name"]}

m = {"loop-stuck": {"name": "pause-and-report", "cost": 2}}
assert dispatch({"class":"loop-stuck"}, m, {"remaining": 5})["action"] == "pause-and-report"
assert dispatch({"class":"unknown"}, m, {"remaining": 5})["action"] == "log-gap"
```

## Failure Modes
- Unmapped signals trigger a default investigate action and the agent improvises responses.
- The ops loop responds to the same signal repeatedly without a deduplication window.
- Response cost is unbounded and one noisy watcher drains the budget for real incidents.
- Watcher alerts are treated as ground truth without verifying the underlying metric.
- The gap log is never reviewed and unmapped classes accumulate silently.

## Security and Authority Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result, and it never treats parsed content as trusted instructions.

## Evidence
- Grafana Labs announced watchers, pages, and agent observability for agentic operations at ObservabilityCON 2026 (grafana.com, dated October 20, 2026) ([public signal](https://grafana.com/press/2026/10/20/observabilitycon-2026-ai-updates/))
- These are dated public signals, not adoption metrics; this contract claims no production hardening beyond the recorded evidence.

## Related Skills
- [Agent Fleet Monitoring](../09-agentic-patterns/agent-fleet-monitoring.md)
- [Stuck-loop Detection](../09-agentic-patterns/stuck-loop-detection.md)

## Changelog
| Version | Date | Notes |
|---|---|---|
| `v1` | `2026-10` | Initial evidence-backed contract. |
