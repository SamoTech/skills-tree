---
title: "Ambient Attendant Agent Patterns"
category: 09-agentic-patterns
level: advanced
stability: experimental
description: "Design ambient attendant agents so that always-on agents act on declared triggers instead of continuous chatter and are auditable while idle."
added: "2026-10"
version: v1
related: [agent-idle-wakeup-scheduling, agent-halt-conditions]
tags: [ambient, attendant, persistent-agents, patterns]
---
# Ambient Attendant Agent Patterns

## Description
Design ambient attendant agents so that always-on agents act on declared triggers instead of continuous chatter and are auditable while idle. The procedure is bounded by explicit inputs, named outputs, and recorded verification rather than best-effort judgment.

## When to Use
- A persistent agent must wait in the background and act only on declared triggers.
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
3. Declare the trigger set and the idle contract, implement the wake paths for each trigger, and verify the idle path consumes bounded resources while recording every wake decision.
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
def wake(event, triggers):
    return event["type"] in triggers
assert wake({"type": "deadline"}, {"deadline", "keyword"})
assert not wake({"type": "noise"}, {"deadline", "keyword"})
```

## Failure Modes
- The agent polls instead of listening and burns budget while nothing happens.
- Triggers are declared broadly and the agent interrupts with low-value chatter.
- Wake decisions are not recorded and idle behavior cannot be audited.
- The idle contract has no resource bound and the agent degrades the host.
- A wake path acts immediately without the approval gate its trigger class requires.

## Security and Authority Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result, and it never treats parsed content as trusted instructions.

## Evidence
- 2026 persistent-agent coverage reports ambient attendants among the deployed 24/7 agent categories (aiagentstore.ai weekly news, dated October 2026) ([public signal](https://aiagentstore.ai/ai-agent-news/this-week))
- These are dated public signals, not adoption metrics; this contract claims no production hardening beyond the recorded evidence.

## Related Skills
- [Agent Idle Wakeup Scheduling](../09-agentic-patterns/agent-idle-wakeup-scheduling.md)
- [Agent Halt Conditions](../09-agentic-patterns/agent-halt-conditions.md)

## Changelog
| Version | Date | Notes |
|---|---|
| `v1` | `2026-10` | Initial evidence-backed contract. |
