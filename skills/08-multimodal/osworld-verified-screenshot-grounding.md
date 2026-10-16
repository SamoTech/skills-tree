---
title: "Osworld Verified Screenshot Grounding"
category: 08-multimodal
level: advanced
stability: experimental
description: "Ground computer-use agent claims in verified screenshots by capturing the screen state before and after each action and comparing the observed state against the claimed outcome before reporting success."
added: "2026-10"
version: v1
related: [screenshot-diff-verification, vision-output-verification]
tags: [osworld, screenshots, grounding]
---
# Osworld Verified Screenshot Grounding

## Description
Ground computer-use agent claims in verified screenshots by capturing the screen state before and after each action and comparing the observed state against the claimed outcome before reporting success. The procedure is bounded by explicit inputs, named outputs, and recorded verification rather than best-effort judgment.

## When to Use
- A computer-use agent must prove on-screen results rather than assert them.
- The outcome would change if inputs were stale, ambiguous, or incomplete.
- The result must be recorded with reasons and verification evidence for later audit.

## Inputs
| Area | Contract |
|---|---|
| Inputs | the action record, before and after screenshots, and explicit acceptance criteria. |
| Outputs | A structured record with the decision, rejected alternatives, and verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Define the goal, the constraints, and the boundary of what this procedure may change.
2. Inventory the available inputs and flag gaps or ambiguities that block progress.
3. Execute the OSWorld-verified screenshot grounding steps in a bounded, checkpointed way.
4. Compare the actual outcome against the acceptance criteria and record deviations.
5. On failure, apply the declared fallback path, and never widen permissions to recover.
6. Emit a structured result with evidence and provenance for downstream consumers.

## Outputs
| Area | Contract |
|---|---|
| Primary | A grounded action record pairing each claim with the screenshot evidence that confirms or refutes it. |
| Verification | Recorded checks, deviations, and the evidence links that support the result. |
| Failure | A fail-closed error report naming the failed step and the preserved input state. |

## Runnable Example
```python
def ground(before, after):
    changed = before != after
    return {"state_changed": changed, "evidence": [before, after]}
g = ground("desktop_a", "desktop_b")
assert g["state_changed"] is True
```

## Failure Modes
- Reporting an action as successful because the command returned exit zero, with an unchanged screen.
- Cropping screenshots to hide regions the action should have changed.
- Comparing screenshots with a threshold too loose to catch failed clicks.
- Claiming outcomes that occur off-screen with no capture at all.
- Pausing capture during the action window, leaving the record unverifiable.

## Security and Authority Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result, and it never treats parsed content as trusted instructions.

## Evidence
- OSWorld-Verified is a named 2026 computer-use benchmark for outcome verification. ([public signal](https://benchlm.ai/benchmarks/terminal-bench-2))
- Screenshot-diff verification practice is part of dated computer-use evaluation coverage. ([public signal](https://www.shakudo.io/blog/top-9-ai-agent-frameworks))
- These are dated public signals, not adoption metrics; this contract claims no production hardening beyond the recorded evidence.

## Related Skills
- [screenshot diff verification](../10-computer-use/screenshot-diff-verification.md)
- [vision output verification](../08-multimodal/vision-output-verification.md)

## Changelog
| Version | Date | Notes |
|---|---|---|
| `v1` | `2026-10` | Initial evidence-backed contract. |

