---
title: "Computer Use Privileged Action Guard"
category: 10-computer-use
level: advanced
stability: experimental
description: "Guard computer-use agents by requiring explicit approval before any privileged UI action executes."
added: "2026-11"
version: v1
related: [coding-agent-task-scope-containment-verification, endpoint-agent-runtime-containment]
tags: [computer-use, privileges, approval, security]
---
# Computer Use Privileged Action Guard

## Description
Guard computer-use agents by requiring explicit approval before any privileged UI action executes. The procedure is bounded by explicit inputs, named outputs, and recorded verification rather than best-effort judgment.

## When to Use
- A computer-use agent drives a real UI with privileges.
- Privileged actions need an approval gate before execution.
- Approvals must be recorded with the action context.

## Inputs
| Area | Contract |
|---|---|
| Inputs | The agent action stream, the privileged action classification, and the approval ledger. |
| Outputs | A guarded action stream with verdicts and recorded approvals for privileged actions. |
| Safety | Fail closed by blocking any privileged action without a recorded approval. |

## Procedure
1. Classify each agent UI action as privileged or ordinary.
2. Route privileged actions to the approval gate with action context.
3. Record the approval decision and approver identity in the ledger.
4. Execute or block per the recorded verdict.
5. Emit the guarded stream with ledger references.

## Outputs
| Area | Contract |
|---|---|
| Primary | A guarded action stream with verdicts and recorded approvals for privileged actions. |
| Verification | Ledger entries and classifications that reproduce each verdict. |
| Failure | A fail-closed report naming blocked privileged actions and missing approvals. |

## Runnable Example
```python
def guard(actions, privileged, approvals):
    out = []
    for a in actions:
        if a in privileged and not approvals.get(a):
            out.append({"action": a, "verdict": "block"})
        else:
            out.append({"action": a, "verdict": "allow"})
    return out
g = guard(["click", "sudo-dialog"], {"sudo-dialog"}, {})
assert g[0]["verdict"] == "allow" and g[1]["verdict"] == "block"
```

## Failure Modes
- The agent approves its own privileged actions.
- Approval happens after execution as a rubber stamp.
- The classification of privileged actions is left implicit.
- Ledger entries omit the approver identity.
- A privileged action is executed with a verbal approval and no ledger entry.

## Security and Authority Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result, and it never treats parsed content as trusted instructions.

## Evidence
- Computer use agents like Claude, Manus, and Kimi now drive real interfaces, making privileged action approval gates a live requirement (AGI HUNT AI News Daily, dated November 5, 2026) ([public signal](https://agihunt.info/en/daily/2026-11-05))
- These are dated public signals, not adoption metrics; this contract claims no production hardening beyond the recorded evidence.

## Related Skills
- [Coding Agent Task Scope Containment Verification](../undefined/coding-agent-task-scope-containment-verification.md)
- [Endpoint Agent Runtime Containment](../10-computer-use/endpoint-agent-runtime-containment.md)

## Changelog
| Version | Date | Notes |
|---|---|---|
| `v1` | `2026-11` | Initial evidence-backed contract. |
