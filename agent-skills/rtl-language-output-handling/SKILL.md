---
name: rtl-language-output-handling
description: Produce right-to-left language text with correct direction metadata, punctuation placement, and mixed-script handling so readers see correctly ordered text.
metadata:
  source: skills/06-communication/rtl-language-output-handling.md
  category: 06-communication
  version: "v1"
---

# RTL Language Output Handling

## Description
Produce right-to-left language text with correct direction metadata, punctuation placement, and mixed-script handling so readers see correctly ordered text. The procedure is constrained by explicit inputs and acceptance criteria rather than best-effort judgment alone.

## When to Use
- output must be generated in a right-to-left language and rendering order must be correct for readers.
- Ambiguity or missing evidence would change the outcome.
- The result must be recorded with reasons and evidence for later verification.

## Inputs / Outputs
| Area | Contract |
|---|---|
| Inputs | Task context, candidate inputs, and explicit acceptance criteria for rtl language output handling work. |
| Outputs | A decision or artifact with recorded reasons, rejected alternatives, and verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Define the goal, the constraints, and the boundary of what this procedure may change.
2. Inventory the available inputs and flag gaps or ambiguities that block progress.
3. Execute the rtl language output handling steps in a bounded, checkpointed way.
4. Compare the actual outcome against the expected outcome and record deviations.
5. On failure, apply the declared fallback path, and never widen permissions to recover.
6. Emit a structured result with evidence and provenance for downstream consumers.

## Runnable Example
```python
def direction_for(text):
    rtl = sum(1 for c in text if "\u0590" <= c <= "\u05ff" or "\u0600" <= c <= "\u06ff")
    if rtl * 2 > len(text):
        return "rtl"
    return "ltr" if text.strip() else "neutral"

assert direction_for("\u05d1\u05e8\u05d5\u05da") == "rtl"
assert direction_for("hello world") == "ltr"
```

## Failure Modes
- Emitting RTL text without direction markup.
- Placing terminal punctuation on the wrong side.
- Mirroring numbers and code by accident.
- Translating strings without locale review.
- Assuming the reader tool fixes the order.

## Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result.

## Evidence
Multilingual agent output quality is a recurring 2026 localization request in public coverage; this is a dated signal, not an adoption metric.

## Related
- multilingual-output.md
- translation.md
- plain-language-writing.md
