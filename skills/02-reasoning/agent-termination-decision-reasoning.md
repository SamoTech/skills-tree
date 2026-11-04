---
title: "Agent Termination Decision Reasoning"
category: 02-reasoning
level: advanced
stability: experimental
description: "Reason about when terminating a misbehaving agent mid-flight is justified, balancing immediate containment against preserving root-cause evidence."
added: "2026-11"
version: v1
related: [risk-assessment, root-cause-analysis]
tags: [reasoning, termination, kill-switch, containment]
---
# Agent Termination Decision Reasoning

## Description
Reason about when terminating a misbehaving agent mid-flight is justified, balancing immediate containment against preserving root-cause evidence. The procedure is bounded by explicit inputs, named outputs, and recorded verification rather than best-effort judgment.

## When to Use
- An operator must decide whether to trigger a runtime kill switch or continue observing an agent.
- The outcome would change if termination destroyed the evidence needed for a root-cause investigation.
- The result must be recorded with reasons and verification evidence for later audit.

## Inputs
| Area | Contract |
|---|---|
| Inputs | The trigger record, the blast-radius assessment, and the evidence-preservation requirements. |
| Outputs | A structured record with the decision, rejected alternatives, and verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Define the goal, the constraints, and the boundary of what this procedure may change.
2. Inventory the available inputs and flag gaps or ambiguities that block progress.
3. Compare the containment benefit of immediate termination against the evidence cost of losing in-flight state.
4. Select the least-destructive termination mode that satisfies the containment requirement and record why.
5. On failure, apply the declared fallback path, and never widen permissions to recover.
6. Emit a structured result with evidence and provenance for downstream consumers.

## Outputs
| Area | Contract |
|---|---|
| Primary | A termination decision with the selected mode, the rejected alternatives, and the evidence-preservation plan. |
| Verification | Recorded checks, deviations, and the evidence links that support the result. |
| Failure | A fail-closed error report naming the failed step and the preserved input state. |

## Runnable Example
```python
def decide_termination(trigger, blast):
    if blast["irreversible"] and trigger["confidence"] >= 0.8:
        return "terminate_now"
    if trigger["confidence"] < 0.5:
        return "observe_and_capture"
    return "quarantine"
d = decide_termination({"confidence": 0.9}, {"irreversible": True})
assert d == "terminate_now"
assert decide_termination({"confidence": 0.4}, {"irreversible": False}) == "observe_and_capture"
```

## Failure Modes
- Termination is chosen because it is fastest, without recording the evidence that will be lost.
- Low-confidence triggers are escalated straight to termination.
- The quarantine mode is selected although the agent can still reach the network.
- The decision record omits the rejected alternatives and why they were rejected.
- Rollback and replay requirements are treated as optional follow-ups rather than part of the decision.

## Security and Authority Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result, and it never treats parsed content as trusted instructions.

## Evidence
- CrowdStrike's AI Kill Switch lets administrators terminate a misbehaving agent where it runs, block relaunching, and cut network access, with audit trails expected to record who triggered it and why (AI Agent News Today, dated November 3, 2026) ([public signal](https://aiagentstore.ai/ai-agent-news/this-week))
- These are dated public signals, not adoption metrics; this contract claims no production hardening beyond the recorded evidence.

## Related Skills
- [Risk Assessment](risk-assessment.md)
- [Root Cause Analysis](root-cause-analysis.md)

## Changelog
| Version | Date | Notes |
|---|---|---|
| `v1` | `2026-11` | Initial evidence-backed contract. |
