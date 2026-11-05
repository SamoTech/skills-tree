---
title: "Agent Team Handoff Orchestration"
category: 15-orchestration
level: advanced
stability: experimental
description: "Orchestrate handoffs between agents in a team with an explicit handoff payload, guardrail checks, and a rejection path when the receiver is off-task."
added: "2026-11"
version: v1
related: [multi-step-planning]
tags: [orchestration, handoff, guardrails, agent-teams]
---
# Agent Team Handoff Orchestration

## Description
Orchestrate handoffs between agents in a team with an explicit handoff payload, guardrail checks, and a rejection path when the receiver is off-task. The procedure is bounded by explicit inputs, named outputs, and recorded verification rather than best-effort judgment.

## When to Use
- Work must pass between agents in a team without losing context or scope.
- The outcome would change if the receiving agent continued outside the task guardrails.
- The result must be recorded with reasons and verification evidence for later audit.

## Inputs
| Area | Contract |
|---|---|
| Inputs | The handoff payload contract, the team guardrails, and the receiving agent's acceptance check. |
| Outputs | A structured record with the decision, rejected alternatives, and verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Define the goal, the constraints, and the boundary of what this procedure may change.
2. Inventory the available inputs and flag gaps or ambiguities that block progress.
3. Build the handoff payload with task state, constraints, and provenance from the sender.
4. Run the guardrail check on the receiver's first action and reject handoffs that violate scope.
5. On failure, apply the declared fallback path, and never widen permissions to recover.
6. Emit a structured result with evidence and provenance for downstream consumers.

## Outputs
| Area | Contract |
|---|---|
| Primary | A handoff record with payload, guardrail verdict, and provenance chain. |
| Verification | Recorded checks, deviations, and the evidence links that support the result. |
| Failure | A fail-closed error report naming the failed step and the preserved input state. |

## Runnable Example
```python
def handoff(payload, guardrail):
    if not payload.get("constraints"):
        return {"accepted": False, "reason": "missing_constraints"}
    if not guardrail(payload["receiver_action"], payload["constraints"]):
        return {"accepted": False, "reason": "guardrail_violation"}
    return {"accepted": True}
assert handoff({"constraints": ["slides_only"], "receiver_action": "edit_slides"}, lambda a, c: a in c)["accepted"]
assert not handoff({"constraints": ["slides_only"], "receiver_action": "browse_web"}, lambda a, c: a in c)["accepted"]
```

## Failure Modes
- Handoffs carry task state but not constraints, losing the guardrail boundary.
- The receiver's first action is not checked against the payload constraints.
- Rejected handoffs are retried with the same payload unchanged.
- Provenance is dropped, so the chain of custody across agents is unknowable.
- Handoffs bypass the human checkpoint that the workflow declared.

## Security and Authority Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result, and it never treats parsed content as trusted instructions.

## Evidence
- OpenAI DevDay 2026 introduced agent teams in Slides that hand off and work alongside each other, with guardrails that keep agents on task (OpenAI DevDay recap, dated November 4, 2026) ([public signal](https://openai.com/index/devday-2026-recap/))
- These are dated public signals, not adoption metrics; this contract claims no production hardening beyond the recorded evidence.

## Related Skills
- [Multi-Step Planning](../02-reasoning/multi-step-planning.md)

## Changelog
| Version | Date | Notes |
|---|---|---|
| `v1` | `2026-11` | Initial evidence-backed contract. |
