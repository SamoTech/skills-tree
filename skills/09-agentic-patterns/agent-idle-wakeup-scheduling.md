---
title: "Agent Idle Wakeup Scheduling"
category: 09-agentic-patterns
level: advanced
stability: experimental
description: "Schedule agent wakeups for deferred work with idempotency keys and stale-wakeup detection so an agent resumes exactly once per trigger."
added: "2026-10"
version: v1
related: [agent-checkpoint-restore-patterns, guardrail-wrapped-agent-loops]
tags: [scheduling, wakeup, idempotency]
---
# Agent Idle Wakeup Scheduling

## Description
Schedule agent wakeups for deferred work with idempotency keys and stale-wakeup detection so an agent resumes exactly once per trigger. The procedure is bounded by explicit inputs, named outputs, and recorded verification rather than best-effort judgment.

## When to Use
- Deferred work must resume later exactly once, even if timers fire twice.
- The outcome would change if inputs were stale, ambiguous, or incomplete.
- The result must be recorded with reasons and verification evidence for later audit.

## Inputs
| Area | Contract |
|---|---|
| Inputs | agent idle wakeup scheduling task context, candidate data, and explicit acceptance criteria. |
| Outputs | A structured record with the decision, rejected alternatives, and verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Define the goal, the constraints, and the boundary of what this procedure may change.
2. Inventory the available inputs and flag gaps or ambiguities that block progress.
3. Execute the agent idle wakeup scheduling steps in a bounded, checkpointed way.
4. Compare the actual outcome against the acceptance criteria and record deviations.
5. On failure, apply the declared fallback path, and never widen permissions to recover.
6. Emit a structured result with evidence and provenance for downstream consumers.

## Outputs
| Area | Contract |
|---|---|
| Primary | A wakeup record with idempotency key, trigger, deadline, and admitted state. |
| Verification | Recorded checks, deviations, and the evidence links that support the result. |
| Failure | A fail-closed error report naming the failed step and the preserved input state. |

## Runnable Example
```python
def admit(wakeup, seen):
    if wakeup["key"] in seen:
        return None
    seen.add(wakeup["key"])
    return wakeup["task"]
seen = set()
assert admit({"key": "k1", "task": "poll"}, seen) == "poll"
assert admit({"key": "k1", "task": "poll"}, seen) is None
```

## Failure Modes
- Resuming work twice because the wakeup carried no idempotency key.
- Executing a wakeup whose deadline already passed without re-checking state.
- Queueing wakeups without recording what each one is waiting for.
- Retrying without preserving state or evidence.
- Reporting success without checking the resulting state.

## Security and Authority Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result, and it never treats parsed content as trusted instructions.

## Evidence
- Idle scheduling and resumption are 2026 agent memory practice themes. ([public signal](https://mem0.ai/blog/state-of-ai-agent-memory-2026))
- These are dated public signals, not adoption metrics; this contract claims no production hardening beyond the recorded evidence.

## Related Skills
- [agent checkpoint restore patterns](../09-agentic-patterns/agent-checkpoint-restore-patterns.md)
- [guardrail wrapped agent loops](../09-agentic-patterns/guardrail-wrapped-agent-loops.md)

## Changelog
| Version | Date | Notes |
|---|---|---|
| `v1` | `2026-10` | Initial evidence-backed contract. |
