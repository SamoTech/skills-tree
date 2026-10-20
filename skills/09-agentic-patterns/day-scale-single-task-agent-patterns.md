---
title: "Day Scale Single Task Agent Patterns"
category: 09-agentic-patterns
level: advanced
stability: experimental
description: "Structure day-scale single tasks so an agent runs long work with checkpoints, budgets, and resumable state instead of one fragile turn."
added: "2026-10"
version: v1
related: [agent-checkpointing, multiday-agent-mission-decomposition-patterns]
tags: [long-running, checkpoints, budgets, patterns]
---
# Day Scale Single Task Agent Patterns

## Description
Structure day-scale single tasks so an agent runs long work with checkpoints, budgets, and resumable state instead of one fragile turn. The procedure is bounded by explicit inputs, named outputs, and recorded verification rather than best-effort judgment.

## When to Use
- A single task is expected to run for hours and must survive provider and context turbulence.
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
3. Decompose the task into checkpointed milestones with a per-milestone budget, define the resume contract from persisted state, and run with halt conditions that trigger human review rather than silent retry loops.
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
def next_milestone(state, milestones):
    for m in milestones:
        if m["name"] not in state["done"]:
            return m if state["budget_left"] >= m["cost"] else None
    return None
ms = [{"name": "extract", "cost": 10}, {"name": "verify", "cost": 5}]
assert next_milestone({"done": ["extract"], "budget_left": 3}, ms) is None
assert next_milestone({"done": ["extract"], "budget_left": 9}, ms)["name"] == "verify"
```

## Failure Modes
- The task runs as one giant turn and any hiccup restarts from zero.
- Checkpoints exist but the resume contract is undefined, so resumption diverges.
- Budgets are set per task rather than per milestone and one runaway milestone consumes the day.
- Halt conditions alert nobody and the agent idles for hours.
- Progress reports are fire-and-forget and nobody sees stalls.

## Security and Authority Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result, and it never treats parsed content as trusted instructions.

## Evidence
- 2026 Notion's agent harness raises single agent task duration from five minutes to more than 24 hours (notion.com, dated October 2026) ([public signal](https://www.notion.com/blog/notion-ai-more-for-less))
- These are dated public signals, not adoption metrics; this contract claims no production hardening beyond the recorded evidence.

## Related Skills
- [Agent Checkpointing](../09-agentic-patterns/agent-checkpointing.md)
- [Multiday Agent Mission Decomposition Patterns](../09-agentic-patterns/multiday-agent-mission-decomposition-patterns.md)

## Changelog
| Version | Date | Notes |
|---|---|
| `v1` | `2026-10` | Initial evidence-backed contract. |
