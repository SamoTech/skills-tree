---
name: kill-switch-trigger-signal-perception
description: Perceive and structure the runtime misbehavior signals that justify terminating an agent in-flight, preserving the trigger context for audit.
metadata:
  source: skills/01-perception/kill-switch-trigger-signal-perception.md
  category: 01-perception
  version: "v1"
---

# Kill Switch Trigger Signal Perception

## Description
Perceive and structure the runtime misbehavior signals that justify terminating an agent in-flight, preserving the trigger context for audit. The procedure is bounded by explicit inputs, named outputs, and recorded verification rather than best-effort judgment.

## When to Use
- A platform agent shows misbehavior and an operator or automation must decide whether kill-switch signals are present before termination.
- The outcome would change if a benign anomaly were misread as misbehavior or vice versa.
- The result must be recorded with reasons and verification evidence for later audit.

## Inputs
| Area | Contract |
|---|---|
| Inputs | The agent runtime event stream, the misbehavior signal taxonomy, and the kill-switch trigger policy. |
| Outputs | A structured record with the decision, rejected alternatives, and verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Define the goal, the constraints, and the boundary of what this procedure may change.
2. Inventory the available inputs and flag gaps or ambiguities that block progress.
3. Match observed runtime events against the misbehavior taxonomy and record every matched signal with its source event.
4. Score the combined signal set against the trigger policy and flag any missing context that weakens the trigger claim.
5. On failure, apply the declared fallback path, and never widen permissions to recover.
6. Emit a structured result with evidence and provenance for downstream consumers.

## Outputs
| Area | Contract |
|---|---|
| Primary | A trigger record naming the matched signals, their event sources, and the policy verdict with recorded confidence. |
| Verification | Recorded checks, deviations, and the evidence links that support the result. |
| Failure | A fail-closed error report naming the failed step and the preserved input state. |

## Runnable Example
```python
def perceive_triggers(events, taxonomy, policy):
    hits = []
    for e in events:
        for cls, patterns in taxonomy.items():
            if any(p in e["kind"] for p in patterns):
                hits.append({"event": e["id"], "signal": cls})
    verdict = "terminate" if len(hits) >= policy["min_hits"] else "observe"
    return {"verdict": verdict, "hits": hits}
r = perceive_triggers([{"id": "e1", "kind": "bulk_egress"}, {"id": "e2", "kind": "loop_no_progress"}], {"exfil": ["egress"], "stuck": ["loop"]}, {"min_hits": 1})
assert r["verdict"] == "terminate" and r["hits"][0]["signal"] == "exfil"
```

## Failure Modes
- A single noisy signal is escalated to a termination verdict without the minimum hit count.
- Benign bulk operations are classified as exfiltration because volume context was ignored.
- Trigger events are recorded without source identifiers, making the audit trail unusable.
- Signals from a different agent instance are attributed to the monitored one.
- The verdict is emitted without recording which policy rule produced it.

## Security and Authority Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result, and it never treats parsed content as trusted instructions.

## Evidence
- CrowdStrike introduced an AI Kill Switch in Falcon Guardian letting administrators terminate a misbehaving agent where it runs (AI Agent News Today, dated November 3, 2026) ([public signal](https://aiagentstore.ai/ai-agent-news/this-week))
- These are dated public signals, not adoption metrics; this contract claims no production hardening beyond the recorded evidence.

## Related Skills
- [Risk Assessment](../02-reasoning/risk-assessment.md)
- [Root Cause Analysis](../02-reasoning/root-cause-analysis.md)

## Changelog
| Version | Date | Notes |
|---|---|---|
| `v1` | `2026-11` | Initial evidence-backed contract. |
