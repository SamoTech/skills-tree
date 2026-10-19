---
title: "Goal Recovery After Context Loss Patterns"
category: 09-agentic-patterns
level: advanced
stability: experimental
description: "Recover pursuit of the active goal after context loss so that the agent rebuilds state from durable records instead of restarting blind."
added: "2026-10"
version: v1
related: [context-rot-detection, agent-checkpointing]
tags: [recovery, context-loss, journals, resilience]
---
# Goal Recovery After Context Loss Patterns

## Description
Recover pursuit of the active goal after context loss so that the agent rebuilds state from durable records instead of restarting blind. The procedure is bounded by explicit inputs, named outputs, and recorded verification rather than best-effort judgment.

## When to Use
- An agent loses its context mid-mission and must continue rather than restart.
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
3. Detect the context loss event, rebuild the working state from the durable journal and goal record, and verify the rebuilt state against the last checkpoint before resuming.
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
def rebuild(journal, checkpoint):
    state = dict(checkpoint)
    for entry in journal[:len(journal)]:
        if entry["seq"] <= state["seq"]:
            continue
        state[entry["key"]] = entry["value"]
        state["seq"] = entry["seq"]
    return state
j = [{"seq": 3, "key": "x", "value": 1}]
assert rebuild(j, {"seq": 2, "x": 0})["x"] == 1
```

## Failure Modes
- Recovery replays the journal from the start and re-executes recorded side effects.
- The rebuilt state skips checkpoint verification and resumes on corrupted data.
- Context loss is detected only on hard crashes, not on silent truncation.
- The goal record itself lived only in the lost context, so nothing remains to recover toward.
- Recovery resumes mid-step instead of at the last recorded boundary and double-executes the step.

## Security and Authority Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result, and it never treats parsed content as trusted instructions.

## Evidence
- 2026 agent memory research covers long-horizon session recovery as a core persistence requirement (mem0.ai, dated October 2026) ([public signal](https://mem0.ai/blog/state-of-ai-agent-memory-2026))
- These are dated public signals, not adoption metrics; this contract claims no production hardening beyond the recorded evidence.

## Related Skills
- [Context Rot Detection](../03-memory/context-rot-detection.md)
- [Agent Checkpointing](../09-agentic-patterns/agent-checkpointing.md)

## Changelog
| Version | Date | Notes |
|---|---|
| `v1` | `2026-10` | Initial evidence-backed contract. |
