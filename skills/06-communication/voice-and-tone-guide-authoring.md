---
title: "Voice And Tone Guide Authoring"
category: 06-communication
level: advanced
stability: experimental
description: "Write machine-usable voice and tone guides with rules, positive and negative examples, and scope exceptions."
added: "2026-10"
version: v1
related: [tone-adjustment, persona-adoption, plain-language-writing]
tags: [voice, and, tone, guide]
---
# Voice And Tone Guide Authoring

## Description
Write machine-usable voice and tone guides with rules, positive and negative examples, and scope exceptions. The procedure is constrained by explicit inputs and acceptance criteria rather than best-effort judgment alone.

## When to Use
- A task requires voice and tone guide authoring before downstream steps can proceed safely.
- Ambiguity or missing evidence would change the outcome.
- The result must be recorded with reasons and evidence for later verification.

## Inputs / Outputs
| Area | Contract |
|---|---|
| Inputs | Task context, candidate inputs, and explicit acceptance criteria for voice and tone guide authoring. |
| Outputs | A decision or artifact with recorded reasons, rejected alternatives, and verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Define the goal, the constraints, and the boundary of what this procedure may change.
2. Inventory the available inputs and flag gaps or ambiguities that block progress.
3. Execute the voice and tone guide authoring steps in a bounded, checkpointed way.
4. Compare the actual outcome against the expected outcome and record deviations.
5. On failure, apply the declared fallback path, and never widen permissions to recover.
6. Emit a structured result with evidence and provenance for downstream consumers.

## Runnable Example
```python
def apply_guide(text, rules):
    for bad, good in rules:
        text = text.replace(bad, good)
    return text
assert apply_guide("Hey!!", [("!!", "!")]) == "Hey!"
```

## Failure Modes
- Acting outside the declared task boundary.
- Assuming an estimate or preview equals the verified effect.
- Retrying without preserving state or evidence.
- Using stale inputs as if they were current.
- Reporting success without checking the resulting state.

## Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result.

## Evidence
Teams building assistant products in 2026 request authoring guides that keep generated copy on-brand. These are dated public signals, not adoption metrics.

## Related
- tone-adjustment.md
- persona-adoption.md
- plain-language-writing.md
