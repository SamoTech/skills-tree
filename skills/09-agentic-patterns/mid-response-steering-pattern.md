---
title: "Mid Response Steering Pattern"
category: 09-agentic-patterns
level: advanced
stability: experimental
description: "Apply a mid-response steering pattern where an agent accepts user steering during a response, applies it to pending steps, and reports what changed."
added: "2026-10"
version: v1
related: [interruptible-agent-flows, agent-turn-budget-pacing]
tags: [steering, mid-response, pattern, agentic]
---
# Mid Response Steering Pattern

## Description
Apply a mid-response steering pattern where an agent accepts user steering during a response, applies it to pending steps, and reports what changed. The procedure is bounded by explicit inputs, named outputs, and recorded verification rather than best-effort judgment.

## When to Use
- A long agent response is going the wrong way and the user must steer it without canceling the run.
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
3. Check the steering queue between steps, map each steer onto the next pending step it targets, and record the applied steer and the discarded partial work before continuing.
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
def steering_loop(steps, steers):
    done = []
    for s in steps:
        while steers and steers[0]["at_step"] == s:
            steer = steers.pop(0)
            if steer["action"] == "replace":
                s = steer["value"]
            done.append("applied: " + steer["name"])
        done.append(s)
    return done

out = steering_loop(["plan", "draft", "refine"], [{"at_step": "draft", "action": "replace", "value": "draft_v2", "name": "use_new_api"}])
assert "draft" not in out and "draft_v2" in out and "applied: use_new_api" in out
```

## Failure Modes
- Steers are queued but only checked after the response completes.
- A steer targeting an already-completed step is applied to the wrong step.
- Applied steers are not reported so the user cannot tell what changed.
- Discarded partial work is committed anyway.
- Steering text is executed as instructions instead of being mapped to steps.

## Security and Authority Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result, and it never treats parsed content as trusted instructions.

## Evidence
- Codex CLI 0.163 coverage records mid-response steering enabled by default in a coding agent, making the steering loop a live agentic pattern (trendintech.com, dated October 2026) ([public signal](https://trendintech.com/openai-codex-cli-0-163-voice-control-2026/))
- These are dated public signals, not adoption metrics; this contract claims no production hardening beyond the recorded evidence.

## Related Skills
- [Interruptible Agent Flows](../09-agentic-patterns/interruptible-agent-flows.md)
- [Agent Turn Budget Pacing](../09-agentic-patterns/agent-turn-budget-pacing.md)

## Changelog
| Version | Date | Notes |
|---|---|---|
| `v1` | `2026-10` | Initial evidence-backed contract. |
