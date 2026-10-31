---
title: "Long Horizon Goal State Resume"
category: 03-memory
level: advanced
stability: experimental
description: "Persist goal state with completed and pending steps so long-horizon agent work resumes deterministically after a crash."
added: "2026-10"
version: v1
related: [agent-employee-roster-memory, agent-scope-session-isolation-memory]
tags: [resume, checkpoints, durability, goals]
---
# Long Horizon Goal State Resume

## Description
Persist goal state with completed and pending steps so long-horizon agent work resumes deterministically after a crash. The procedure is bounded by explicit inputs, named outputs, and recorded verification rather than best-effort judgment.

## When to Use
- An agent pursues a multi-day goal and must resume exactly where it stopped after a restart rather than repeating or skipping steps.
- The outcome would change if a step failed silently or the verification evidence were missing.
- The result must be recorded with reasons and verification evidence for later audit.

## Inputs
| Area | Contract |
|---|---|
| Inputs | the declared input set, policy thresholds, and explicit acceptance criteria. |
| Outputs | A structured record with the decision, rejected alternatives, and verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Define the goal, the constraints, and the boundary of what this procedure may change.
2. Inventory the available inputs and flag gaps or ambiguities that block progress.
3. Checkpoint the goal with completed and pending step identifiers after every step boundary, then reload the checkpoint on resume and verify the cursor against the recorded progress before executing the next step.
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
def save_resume_state(goal, completed_steps, pending_steps):
    return {"goal": goal, "completed": list(completed_steps), "pending": list(pending_steps)}
def resume_from(state):
    return state["pending"][0] if state["pending"] else None
state = save_resume_state("migrate-db", ["export", "transform"], ["import", "verify"])
assert resume_from(state) == "import" and len(state["completed"]) == 2
```

## Failure Modes
- Progress is checkpointed only at goal completion so a crash restarts the whole run.
- A step is marked completed before its verification and the resume skips a never-finished step.
- The pending list is rebuilt from stale memory and already-completed work is re-executed with side effects.
- Two workers resume the same checkpoint and duplicate the pending steps without a lease check.
- The checkpoint schema changes without a migration and old resume states fail to load mid-goal.

## Security and Authority Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result, and it never treats parsed content as trusted instructions.

## Evidence
- the mid-October open-source release wave shipped durable resume, goals, and schedules as primitives so solo operators can adopt long-running agents one capability at a time (Reinventing.ai insights, dated October 20, 2026) ([public signal](https://insights.reinventing.ai/articles/ai-agents-open-source-tooling-wave-2026-10-20))
- These are dated public signals, not adoption metrics; this contract claims no production hardening beyond the recorded evidence.

## Related Skills
- [Agent Employee Roster Memory](agent-employee-roster-memory.md)
- [Agent Scope Session Isolation Memory](agent-scope-session-isolation-memory.md)

## Changelog
| Version | Date | Notes |
|---|---|---|
| `v1` | `2026-10` | Initial evidence-backed contract. |
