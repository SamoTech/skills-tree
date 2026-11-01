---
title: "Laboratory Workflow Execution Gating"
category: 04-action-execution
level: advanced
stability: experimental
description: "Gate an agent’s control of laboratory experiments behind approval steps so broad requests become validated procedures with complete records."
added: "2026-10"
version: v1
related: [sandbox-monitor-manipulation-containment, agent-gateway-spend-cap-enforcement]
tags: [laboratory, gating, approval, safety]
---
# Laboratory Workflow Execution Gating

## Description
Gate an agent’s control of laboratory experiments behind approval steps so broad requests become validated procedures with complete records. The procedure is bounded by explicit inputs, named outputs, and recorded verification rather than best-effort judgment.

## When to Use
- An agent connected to laboratory execution systems could modify experiments or test parameters and that authority must be gated.
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
3. Start the agent on low-risk scheduling and retrieval tasks, require an approval gate with a preserved request record before experiment control, and block parameter modification without a human decision.
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
def gate(task, approved_tasks):
    if task["kind"] == "modify-parameters" and task["id"] not in approved_tasks:
        return {"ok": False, "reason": "needs-approval"}
    return {"ok": True}
assert gate({"kind": "schedule", "id": "t1"}, set())["ok"] is True
assert gate({"kind": "modify-parameters", "id": "t2"}, set())["reason"] == "needs-approval"
```

## Failure Modes
- The agent receives full experiment control from day one.
- Approval decisions are not logged with the request they covered.
- Gates are bypassed under deadline pressure without a recorded exception.
- Records are incomplete so the approval trail cannot be reconstructed.
- All tasks are treated as low-risk without a tiering pass.

## Security and Authority Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result, and it never treats parsed content as trusted instructions.

## Evidence
- the Waters AI Link guidance to start with low-risk scheduling, setup, or data-retrieval tasks and require approval gates and complete records before allowing an agent to control experiments or modify test parameters (Waters blog, dated October 31, 2026) ([public signal](https://www.waters.com/blog/from-complex-workflows-to-conversation-how-waters-is-bringing-governed-practical-ai-into-laboratory-software/))
- These are dated public signals, not adoption metrics; this contract claims no production hardening beyond the recorded evidence.

## Related Skills
- [Sandbox Monitor Manipulation Containment](sandbox-monitor-manipulation-containment.md)
- [Agent Gateway Spend Cap Enforcement](agent-gateway-spend-cap-enforcement.md)

## Changelog
| Version | Date | Notes |
|---|---|---|
| `v1` | `2026-10` | Initial evidence-backed contract. |
