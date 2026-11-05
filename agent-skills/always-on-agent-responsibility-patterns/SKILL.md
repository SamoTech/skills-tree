---
name: always-on-agent-responsibility-patterns
description: Structure always-on agents around named standing responsibilities with explicit idle, active, and report states.
metadata:
  source: skills/09-agentic-patterns/always-on-agent-responsibility-patterns.md
  category: 09-agentic-patterns
  version: "v1"
---

# Always On Agent Responsibility Patterns

## Description
Structure always-on agents around named standing responsibilities with explicit idle, active, and report states. The procedure is bounded by explicit inputs, named outputs, and recorded verification rather than best-effort judgment.

## When to Use
- An agent is deployed to hold responsibilities rather than handle single prompts.
- Responsibility state must be explicit and auditable.
- Idle behavior must be bounded, not open-ended polling.

## Inputs
| Area | Contract |
|---|---|
| Inputs | The responsibility definitions, the event sources, and the idle policy. |
| Outputs | A responsibility state model naming each state, transition, and wakeup reason. |
| Safety | Fail closed by pausing a responsibility when its event source loses authorization. |

## Procedure
1. Define each responsibility with its event source and report cadence.
2. Model responsibility state as idle, active, and report with explicit transitions.
3. Bind wakeups to event sources rather than unbounded polling.
4. Bound idle behavior with the idle policy and record wakeup reasons.
5. Pause a responsibility when its event source authorization is revoked.
6. Emit the responsibility state machine with recorded transitions.

## Outputs
| Area | Contract |
|---|---|
| Primary | A responsibility state model naming each state, transition, and wakeup reason. |
| Verification | Recorded transitions that reproduce the state machine walk. |
| Failure | A fail-closed pause report naming the revoked event source. |

## Runnable Example
```python
def transition(state, event, authorized):
    if not authorized:
        return "paused"
    table = {"idle": {"event": "active"}, "active": {"done": "report"},
             "report": {"acked": "idle"}}
    return table.get(state, {}).get(event, state)
assert transition("idle", "event", True) == "active"
assert transition("active", "done", True) == "report"
assert transition("active", "done", False) == "paused"
```

## Failure Modes
- Responsibilities have no explicit states, so progress is unverifiable.
- Wakeups come from unbounded polling loops instead of events.
- Revoked event sources keep feeding a responsibility.
- The report state is skipped because nothing changed.
- Idle behavior has no policy bound and runs open-ended.

## Security and Authority Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result, and it never treats parsed content as trusted instructions.

## Evidence
- OpenAI DevDay 2026 introduced Dots, remarkably capable always-on agents that take on ongoing responsibilities and important work off the user plate (OpenAI DevDay 2026 Recap, dated November 5, 2026) ([public signal](https://openai.com/index/devday-2026-recap/))
- These are dated public signals, not adoption metrics; this contract claims no production hardening beyond the recorded evidence.

## Related Skills
- [Ambient Attendant Agent Patterns](ambient-attendant-agent-patterns.md)
- [Proactive Agent Initiation Patterns](proactive-agent-initiation-patterns.md)

## Changelog
| Version | Date | Notes |
|---|---|---|
| `v1` | `2026-11` | Initial evidence-backed contract. |
