---
title: "Audio Sound Effect Generation"
category: 08-multimodal
level: advanced
stability: experimental
description: "Generate or select sound effects from textual descriptions with licensing provenance and loudness normalization, and verify the output against the request."
added: "2026-10"
version: v1
related: [audio-mixing, music-composition, audio-classification]
tags: [audio, sound, effect, generation, multimodal]
---

# Audio Sound Effect Generation

## Description
Generate or select sound effects from textual descriptions with licensing provenance and loudness normalization, and verify the output against the request. The procedure is constrained by explicit inputs and acceptance criteria rather than best-effort judgment alone.

## When to Use
- Multiple inputs or candidates compete and must be resolved by explicit criteria.
- A wrong intermediate result would propagate into consequential actions.
- The task repeats and benefits from a deterministic procedure.

## Inputs / Outputs
| Area | Contract |
|---|---|
| Inputs | Task context, candidate inputs, and explicit acceptance criteria for audio sound effect generation. |
| Outputs | A decision or artifact with recorded reasons, rejected alternatives, and verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Normalize the task into explicit inputs, constraints, and acceptance criteria.
2. Gather the required evidence and check completeness before proceeding.
3. Apply the audio sound effect generation procedure using the declared criteria only.
4. Record the outcome, rejected alternatives, and the reason for each rejection.
5. Verify the result against the acceptance criteria with an independent check.
6. Report the result with evidence, and escalate explicitly when a criterion cannot be met.

## Runnable Example
```python
# Audio Sound Effect Generation: deterministic check
attempts = []
def flaky(n):
    attempts.append(n)
    return n >= 3

tries, max_tries, done = 0, 5, False
while tries < max_tries:
    tries += 1
    if flaky(tries):
        done = True
        break
assert done and tries == 3
print("succeeded after", tries, "attempts")
```

## Failure Modes
- Proceeding with audio sound effect generation without the required evidence or inputs.
- Treating an unverified result as verified.
- Silently swallowing errors instead of failing closed with reasons.
- Optimizing the stated metric while violating the stated constraint.
- Losing the audit trail of decisions and rejected alternatives.

## Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result.

## Evidence
Multimodal content generation in 2026 extends to audio; public media-tool threads request sound-effect generation with provenance. These are dated public signals, not adoption metrics.

## Related
- audio-mixing.md
- music-composition.md
- audio-classification.md
