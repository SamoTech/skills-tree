---
title: "A2a Remote Agent Delegation Pattern"
category: 09-agentic-patterns
level: advanced
stability: experimental
description: "Apply the A2A remote agent delegation pattern so tasks cross agent boundaries with declared state and lifecycle rules."
added: "2026-10"
version: v1
related: [agent-as-tool, agent-checkpoint-restore-patterns]
tags: [a2a, delegation, patterns, lifecycle]
---
# A2a Remote Agent Delegation Pattern

## Description
Apply the A2A remote agent delegation pattern so tasks cross agent boundaries with declared state and lifecycle rules. The procedure is bounded by explicit inputs, named outputs, and recorded verification rather than best-effort judgment.

## When to Use
- A task must be delegated to a remote A2A agent and the delegation needs a repeatable lifecycle pattern.
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
3. Instantiate the delegation with a task id and declared state machine, propagate the required context, and track the task through its recorded lifecycle states.
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
def delegate_task(remote, task, states):
    tid = remote.submit(task)
    state = remote.status(tid)
    if state not in states:
        raise ValueError("undeclared task state: " + state)
    return {"task": tid, "state": state}
remote = {"submit": lambda t: "task-1", "status": lambda t: "submitted"}
assert delegate_task(remote, {"goal": "summarize"}, {"submitted", "working", "done"})["state"] == "submitted"
```

## Failure Modes
- Delegated tasks carry no declared state machine and completed work cannot be distinguished from lost work.
- Context is propagated without the task boundary and the remote agent sees out-of-scope data.
- Task ids are not recorded and delegations cannot be reconciled after a crash.
- The pattern assumes synchronous completion and hangs on long remote tasks.
- Remote failures surface as generic errors and the delegating agent retries without idempotency.

## Security and Authority Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result, and it never treats parsed content as trusted instructions.

## Evidence
- The Agentic AI Foundation announcement records A2A joining AAIF as an open agentic stack project governed at the foundation (aaif.io, dated August 17, 2026) ([public signal](https://aaif.io/blog/a2a-joins-aaif))
- These are dated public signals, not adoption metrics; this contract claims no production hardening beyond the recorded evidence.

## Related Skills
- [Agent As Tool](../09-agentic-patterns/agent-as-tool.md)
- [Agent Checkpoint Restore Patterns](../09-agentic-patterns/agent-checkpoint-restore-patterns.md)

## Changelog
| Version | Date | Notes |
|---|---|---|
| `v1` | `2026-10` | Initial evidence-backed contract. |
