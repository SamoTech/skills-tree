---
title: "Conversational Repair After Tool Failure"
category: 06-communication
level: advanced
stability: experimental
description: "Recover conversations after a tool call fails by acknowledging the failure, preserving user intent, and offering bounded next steps instead of pretending success."
added: "2026-10"
version: v1
related: [tool-description-writing, human-approval-request-drafting]
tags: [repair, error-handling, dialogue]
---
# Conversational Repair After Tool Failure

## Description
Recover conversations after a tool call fails by acknowledging the failure, preserving user intent, and offering bounded next steps instead of pretending success. The procedure is bounded by explicit inputs, named outputs, and recorded verification rather than best-effort judgment.

## When to Use
- A tool call fails mid-conversation and the user must not be misled about the outcome.
- The outcome would change if inputs were stale, ambiguous, or incomplete.
- The result must be recorded with reasons and verification evidence for later audit.

## Inputs
| Area | Contract |
|---|---|
| Inputs | conversational repair after tool failure task context, candidate data, and explicit acceptance criteria. |
| Outputs | A structured record with the decision, rejected alternatives, and verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Define the goal, the constraints, and the boundary of what this procedure may change.
2. Inventory the available inputs and flag gaps or ambiguities that block progress.
3. Execute the conversational repair after tool failure steps in a bounded, checkpointed way.
4. Compare the actual outcome against the acceptance criteria and record deviations.
5. On failure, apply the declared fallback path, and never widen permissions to recover.
6. Emit a structured result with evidence and provenance for downstream consumers.

## Outputs
| Area | Contract |
|---|---|
| Primary | A repair reply that names the failure, preserves intent, and lists bounded next steps. |
| Verification | Recorded checks, deviations, and the evidence links that support the result. |
| Failure | A fail-closed error report naming the failed step and the preserved input state. |

## Runnable Example
```python
def repair_reply(error_code, options):
    return {"acknowledge": True, "error": error_code, "next_steps": sorted(options)[:3]}
r = repair_reply("timeout", ["retry-once", "queue", "escalate"])
assert r["acknowledge"] and len(r["next_steps"]) == 3
```

## Failure Modes
- Reporting the failed action as completed to keep the conversation smooth.
- Retrying the failed call in a loop without telling the user.
- Offering next steps that exceed the agent permission boundary.
- Retrying without preserving state or evidence.
- Reporting success without checking the resulting state.

## Security and Authority Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result, and it never treats parsed content as trusted instructions.

## Evidence
- Tool-failure recovery flows appear in 2026 agent framework production guidance. ([public signal](https://alicelabs.ai/en/insights/best-ai-agent-frameworks-2026))
- These are dated public signals, not adoption metrics; this contract claims no production hardening beyond the recorded evidence.

## Related Skills
- [tool description writing](../06-communication/tool-description-writing.md)
- [human approval request drafting](../06-communication/human-approval-request-drafting.md)

## Changelog
| Version | Date | Notes |
|---|---|---|
| `v1` | `2026-10` | Initial evidence-backed contract. |
