---
title: "Computer Use Approval Gate Automation"
category: 10-computer-use
level: advanced
stability: experimental
description: "Automate the approval gate in front of consequential computer-use actions so pre-action approval is verified per action class."
added: "2026-10"
version: v1
related: [computer-use-agent-human-in-the-loop-approval-operations, human-approval-gate-implementation]
tags: [computer, use, approval, gate, automation]
---
# Computer Use Approval Gate Automation

## Description
Automate the approval gate in front of consequential computer-use actions so pre-action approval is verified per action class. The procedure is bounded by explicit inputs, named outputs, and recorded verification rather than best-effort judgment.

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
3. Classify each pending action against the declared consequence table, route consequential actions to the human gate with a screenshot and the intended target, and block execution until an explicit approval record exists.
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
def gate(action, consequence, approvals):
    if consequence.get(action["kind"]) != "consequential":
        return "auto-execute"
    if approvals.get(action["id"]) is True:
        return "execute"
    return "blocked"

a = {"id": "x1", "kind": "file-delete"}
cons = {"file-delete": "consequential", "scroll": "routine"}
assert gate(a, cons, {}) == "blocked"
assert gate(a, cons, {"x1": True}) == "execute"
```

## Failure Modes
- The consequence table is empty by default and every action auto-executes.
- Approval is granted for the session and later file deletions skip the gate.
- The screenshot presented for approval is captured after the action began.
- Routine actions are reclassified as consequential by a stale table and approval fatigue sets in.
- The gate blocks but queues the action and an approved stale action executes hours later.

## Security and Authority Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result, and it never treats parsed content as trusted instructions.

## Evidence
- Production analyses document approval gates as the operating pattern for safe browser and computer-use agents (lumisai.space, dated October 2026) ([public signal](https://www.lumisai.space/articles/browser-computer-use-agents-2026))
- A safety-focused guide covers what works for browser and computer-use agents in 2026 (lumisai.space, dated October 2026) ([public signal](https://www.lumisai.space/articles/browser-computer-use-agents-2026))
- These are dated public signals, not adoption metrics; this contract claims no production hardening beyond the recorded evidence.

## Related Skills
- [Computer Use Agent Human-in-the-loop Approval Operations](../10-computer-use/computer-use-agent-human-in-the-loop-approval-operations.md)
- [Human Approval Gate Implementation](../04-action-execution/human-approval-gate-implementation.md)

## Changelog
| Version | Date | Notes |
|---|---|---|
| `v1` | `2026-10` | Initial evidence-backed contract. |
