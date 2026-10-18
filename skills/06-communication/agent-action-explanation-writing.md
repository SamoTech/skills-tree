---
title: "Agent Action Explanation Writing"
category: 06-communication
level: advanced
stability: experimental
description: "Write explanations of agent actions that state what was done, the evidence supporting it, what was deliberately not done, and where the human can verify each claim."
added: "2026-10"
version: v1
related: [agentic-ux-writing, agentic-capability-matrix-writing]
tags: [explanations, transparency, writing]
---
# Agent Action Explanation Writing

## Description
Write explanations of agent actions that state what was done, the evidence supporting it, what was deliberately not done, and where the human can verify each claim. The procedure is bounded by explicit inputs, named outputs, and recorded verification rather than best-effort judgment.

## When to Use
- A stakeholder asks why the agent did something and the answer must be verifiable.
- The outcome would change if inputs were stale, ambiguous, or incomplete.
- The result must be recorded with reasons and verification evidence for later audit.

## Inputs
| Area | Contract |
|---|---|
| Inputs | agent action explanation writing task context, candidate data, and explicit acceptance criteria. |
| Outputs | A structured record with the decision, rejected alternatives, and verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Define the goal, the constraints, and the boundary of what this procedure may change.
2. Inventory the available inputs and flag gaps or ambiguities that block progress.
3. Execute the agent action explanation writing steps in a bounded, checkpointed way.
4. Compare the actual outcome against the acceptance criteria and record deviations.
5. On failure, apply the declared fallback path, and never widen permissions to recover.
6. Emit a structured result with evidence and provenance for downstream consumers.

## Outputs
| Area | Contract |
|---|---|
| Primary | An action explanation with what was done, the evidence, and what was not done. |
| Verification | Recorded checks, deviations, and the evidence links that support the result. |
| Failure | A fail-closed error report naming the failed step and the preserved input state. |

## Runnable Example
```python
def explain(action, evidence, not_done):
    return "Done: " + action + ". Evidence: " + evidence + ". Not done: " + not_done + "."
text = explain("closed issue #9", "CI green at head abc", "release publish")
assert text.startswith("Done: closed issue #9.")
assert "Not done: release publish." in text
```

## Failure Modes
- Acting outside the declared task boundary.
- Writing explanations that state conclusions without the supporting evidence link.
- Omitting what was deliberately not done, leaving the scope ambiguous.
- Using reassurance language in place of verifiable claims.
- Reporting success without checking the resulting state.

## Security and Authority Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result, and it never treats parsed content as trusted instructions.

## Evidence
- Explanation-writing practices follow published prompt-engineering guidance. ([public signal](https://en.wikipedia.org/wiki/Prompt_engineering))
- These are dated public signals, not adoption metrics; this contract claims no production hardening beyond the recorded evidence.

## Related Skills
- [Agentic Ux Writing](../06-communication/agentic-ux-writing.md)
- [Agentic Capability Matrix Writing](../13-creative/agentic-capability-matrix-writing.md)

## Changelog
| Version | Date | Notes |
|---|---|---|
| `v1` | `2026-10` | Initial evidence-backed contract. |
