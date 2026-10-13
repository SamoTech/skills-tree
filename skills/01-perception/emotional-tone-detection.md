---
title: "Emotional Tone Detection"
category: 01-perception
level: advanced
stability: experimental
description: "Estimate the emotional tone of text or transcribed speech with explicit confidence and category boundaries, and decline single-label claims the evidence cannot support."
added: "2026-10"
version: v1
related: [intent-classification, keyphrase-extraction, conversation-history-reading]
tags: [tone, nlp, classification]
---

# Emotional Tone Detection

## Description
Estimate the emotional tone of text or transcribed speech with explicit confidence and category boundaries, and decline single-label claims the evidence cannot support. The procedure is constrained by explicit inputs and acceptance criteria rather than best-effort judgment alone.

## When to Use
- a response strategy depends on an explicit, checkable tone estimate before downstream steps can proceed safely.
- Ambiguity or missing evidence would change the outcome.
- The result must be recorded with reasons and evidence for later verification.

## Inputs / Outputs
| Area | Contract |
|---|---|
| Inputs | Task context, candidate inputs, and explicit acceptance criteria for emotional tone detection work. |
| Outputs | A decision or artifact with recorded reasons, rejected alternatives, and verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Define the goal, the constraints, and the boundary of what this procedure may change.
2. Inventory the available inputs and flag gaps or ambiguities that block progress.
3. Execute the emotional tone detection steps in a bounded, checkpointed way.
4. Compare the actual outcome against the expected outcome and record deviations.
5. On failure, apply the declared fallback path, and never widen permissions to recover.
6. Emit a structured result with evidence and provenance for downstream consumers.

## Runnable Example
```python
def classify_tone(score, abstain_low=0.4, abstain_high=0.6):
    if abstain_low <= score <= abstain_high:
        return "abstain"
    return "negative" if score < abstain_low else "positive"

assert classify_tone(0.9) == "positive"
assert classify_tone(0.1) == "negative"
assert classify_tone(0.5) == "abstain"
```

## Failure Modes
- Presenting a soft estimate as a measured fact.
- Ignoring cultural and language variance in tone norms.
- Collapsing mixed tone into a single label.
- Using tone detection to infer unstated user traits.
- Missing the abstain band and forcing a label.

## Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result.

## Evidence
Empathetic agent communication is a recurring 2026 assistant design topic in public coverage; this is a dated signal, not an adoption metric.

## Related
- intent-classification.md
- keyphrase-extraction.md
- conversation-history-reading.md
