---
title: "FAQ Generation"
category: 06-communication
level: advanced
stability: experimental
description: "Build a FAQ from real questions and failure reports, with each answer traceable to its source question and kept synchronized with the underlying behavior."
added: "2026-10"
version: v1
related: [question-answering, summarization, structured-output]
tags: [faq, generation, communication]
---

# FAQ Generation

## Description
Build a FAQ from real questions and failure reports, with each answer traceable to its source question and kept synchronized with the underlying behavior. The procedure is constrained by explicit inputs and acceptance criteria rather than best-effort judgment alone.

## When to Use
- Multiple inputs or candidates compete and must be resolved by explicit criteria.
- A wrong intermediate result would propagate into consequential actions.
- The task repeats and benefits from a deterministic procedure.

## Inputs / Outputs
| Area | Contract |
|---|---|
| Inputs | Task context, candidate inputs, and explicit acceptance criteria for faq generation. |
| Outputs | A decision or artifact with recorded reasons, rejected alternatives, and verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Define the goal, the constraints, and the boundary of what this procedure may change.
2. Inventory the available inputs and flag gaps or ambiguities that block progress.
3. Execute the faq generation steps in a bounded, checkpointed way.
4. Compare the actual outcome against the expected outcome and record deviations.
5. On failure, apply the declared fallback path, and never widen permissions to recover.
6. Emit a structured result with evidence and provenance for downstream consumers.

## Runnable Example
```python
# FAQ Generation: deterministic check
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
- Acting outside the declared task boundary.
- Assuming an estimate or preview equals the verified effect.
- Retrying without preserving state or evidence.
- Using stale inputs as if they were current.
- Reporting success without checking the resulting state.

## Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result.

## Evidence
Support-automation requests in 2026 include FAQ drafting from issue and ticket history. These are dated public signals, not adoption metrics.

## Related
- question-answering.md
- summarization.md
- structured-output.md
