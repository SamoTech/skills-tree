---
title: "VM Sandbox Action Audit Automation"
category: 10-computer-use
level: advanced
stability: experimental
description: "Automate the audit trail of a VM-sandboxed computer-use agent so every action is recorded with its trigger, target, and result state."
added: "2026-10"
version: v1
related: [sandboxed-desktop-vm-execution, computer-use-action-trace-recording]
tags: [vm, sandbox, action, audit, automation]
---
# VM Sandbox Action Audit Automation

## Description
Automate the audit trail of a VM-sandboxed computer-use agent so every action is recorded with its trigger, target, and result state. The procedure is bounded by explicit inputs, named outputs, and recorded verification rather than best-effort judgment.

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
3. Instrument the VM action boundary so each action emits an audit record before execution, attach the result state after execution, and fail the session if any action lacks its before and after records.
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
def audit_gate(actions, records):
    covered = {r["action_id"] for r in records if r.get("before") and r.get("after")}
    missing = [a["id"] for a in actions if a["id"] not in covered]
    if missing:
        raise AssertionError("unaudited actions: " + repr(missing))
    return "sealed"

acts = [{"id":"a1"},{"id":"a2"}]
recs = [{"action_id":"a1","before":True,"after":True},{"action_id":"a2","before":True,"after":True}]
assert audit_gate(acts, recs) == "sealed"
```

## Failure Modes
- The audit record is written after execution and a crashed action leaves no trace.
- Before-state snapshots capture only the active window and out-of-focus changes are missed.
- Audit records are stored inside the same VM they audit and a compromise erases its own trail.
- Actions are batched into one record and individual attribution is lost.
- The session seals with missing records because the audit check is a warning, not a gate.

## Security and Authority Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result, and it never treats parsed content as trusted instructions.

## Evidence
- A production architecture guide documents VM, audit, and recovery for computer-use agents (appscale.blog, dated October 2026) ([public signal](https://appscale.blog/en/blog/computer-use-agent-production-architecture-vm-sandbox-action-audit-2026))
- These are dated public signals, not adoption metrics; this contract claims no production hardening beyond the recorded evidence.

## Related Skills
- [Sandboxed Desktop VM Execution](../10-computer-use/sandboxed-desktop-vm-execution.md)
- [Computer Use Action Trace Recording](../04-action-execution/computer-use-action-trace-recording.md)

## Changelog
| Version | Date | Notes |
|---|---|---|
| `v1` | `2026-10` | Initial evidence-backed contract. |
