---
title: "Background Agent Resilient Execution Pattern"
category: 09-agentic-patterns
level: advanced
stability: experimental
description: "Structure a background agent run so cancellation, provider restart, and history loss degrade to declared fallbacks instead of silent drift."
added: "2026-10"
version: v1
related: [agent-halt-condition, interruptible-agent-flow]
tags: [background, agent, resilient, execution, pattern]
---
# Background Agent Resilient Execution Pattern

## Description
Structure a background agent run so cancellation, provider restart, and history loss degrade to declared fallbacks instead of silent drift. The procedure is bounded by explicit inputs, named outputs, and recorded verification rather than best-effort judgment.

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
3. Declare the run's checkpoint boundary and cancellation surface, verify that cancellation propagates to every in-flight operation, and require the run to re-enter from its last committed checkpoint after any interruption.
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
def reenter(checkpoints, interruption):
    valid = [c for c in checkpoints if c["seq"] <= interruption["at_seq"] and c["committed"]]
    if not valid:
        raise ValueError("no committed checkpoint before interruption")
    return valid[-1]["seq"]

cps = [{"seq":1,"committed":True},{"seq":2,"committed":False},{"seq":3,"committed":True}]
assert reenter(cps, {"at_seq": 3}) == 3
```

## Failure Modes
- Cancellation is honored at the loop level only and an in-flight tool call runs to completion.
- Checkpoint writes are uncommitted and the run re-enters from an earlier state, replaying side effects.
- History loss is handled by silently trimming the prompt and the agent re-plans against corrupted context.
- The restart path is never exercised in tests and the first real provider restart deadlocks the run.
- Background runs share mutable state with foreground sessions and cancellation crosses the boundary.

## Security and Authority Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result, and it never treats parsed content as trusted instructions.

## Evidence
- Agent Framework 1.24.0 honors cancellation while waiting for background agents, the exact resilience defect class this pattern guards (releasebot.io, dated October 7, 2026) ([public signal](https://releasebot.io/updates/microsoft/agent-framework))
- The October framework review documents resilient background execution and Python background agents (developersdigest.tech, dated October 24, 2026) ([public signal](https://www.developersdigest.tech/blog/microsoft-agent-framework-whats-new-2026))
- These are dated public signals, not adoption metrics; this contract claims no production hardening beyond the recorded evidence.

## Related Skills
- [Agent Halt Condition](../09-agentic-patterns/agent-halt-conditions.md)
- [Interruptible Agent Flow](../09-agentic-patterns/interruptible-agent-flows.md)

## Changelog
| Version | Date | Notes |
|---|---|---|
| `v1` | `2026-10` | Initial evidence-backed contract. |
