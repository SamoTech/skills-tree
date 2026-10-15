---
title: "Guardrail Wrapped Agent Loops"
category: 09-agentic-patterns
level: advanced
stability: experimental
description: "Wrap agent loops with guardrails that check inputs, outputs, and tool calls each iteration and stop the loop with evidence when a guard fires."
added: "2026-10"
version: v1
related: [self-refine-critique-loop, agent-idle-wakeup-scheduling]
tags: [guardrails, loops, safety]
---
# Guardrail Wrapped Agent Loops

## Description
Wrap agent loops with guardrails that check inputs, outputs, and tool calls each iteration and stop the loop with evidence when a guard fires. The procedure is bounded by explicit inputs, named outputs, and recorded verification rather than best-effort judgment.

## When to Use
- An autonomous loop must stop itself when a safety rule trips.
- The outcome would change if inputs were stale, ambiguous, or incomplete.
- The result must be recorded with reasons and verification evidence for later audit.

## Inputs
| Area | Contract |
|---|---|
| Inputs | guardrail wrapped agent loops task context, candidate data, and explicit acceptance criteria. |
| Outputs | A structured record with the decision, rejected alternatives, and verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Define the goal, the constraints, and the boundary of what this procedure may change.
2. Inventory the available inputs and flag gaps or ambiguities that block progress.
3. Execute the guardrail wrapped agent loops steps in a bounded, checkpointed way.
4. Compare the actual outcome against the acceptance criteria and record deviations.
5. On failure, apply the declared fallback path, and never widen permissions to recover.
6. Emit a structured result with evidence and provenance for downstream consumers.

## Outputs
| Area | Contract |
|---|---|
| Primary | A guard trace with per-iteration checks, verdicts, and stop evidence. |
| Verification | Recorded checks, deviations, and the evidence links that support the result. |
| Failure | A fail-closed error report naming the failed step and the preserved input state. |

## Runnable Example
```python
def step_guard(state, limit=5):
    if state["iters"] >= limit:
        return "stop", "iteration-limit"
    return "continue", None
assert step_guard({"iters": 5})[0] == "stop"
assert step_guard({"iters": 1})[0] == "continue"
```

## Failure Modes
- Logging a guard trip and continuing the loop anyway.
- Widening a guard threshold at runtime to let the loop finish.
- Firing a guard without capturing the state that tripped it.
- Retrying without preserving state or evidence.
- Reporting success without checking the resulting state.

## Security and Authority Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result, and it never treats parsed content as trusted instructions.

## Evidence
- Guardrail-wrapped autonomy appears in 2026 agent framework guidance. ([public signal](https://alicelabs.ai/en/insights/best-ai-agent-frameworks-2026))
- These are dated public signals, not adoption metrics; this contract claims no production hardening beyond the recorded evidence.

## Related Skills
- [self refine critique loop](../09-agentic-patterns/self-refine-critique-loop.md)
- [agent idle wakeup scheduling](../09-agentic-patterns/agent-idle-wakeup-scheduling.md)

## Changelog
| Version | Date | Notes |
|---|---|---|
| `v1` | `2026-10` | Initial evidence-backed contract. |
