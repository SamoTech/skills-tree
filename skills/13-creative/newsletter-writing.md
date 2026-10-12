---
title: "Newsletter Writing"
category: 13-creative
level: basic
stability: experimental
description: "Write issues of recurring newsletters with a stable structure, honest source links, and audience-consistent tone."
added: "2026-10"
version: v1
related: [blog-writing, copywriting, social-media-post]
tags: [newsletters, writing, content, audience]
---

# Newsletter Writing

## Description
Write issues of recurring newsletters with a stable structure, honest source links, and audience-consistent tone. The procedure is constrained by explicit inputs and acceptance criteria rather than best-effort judgment alone.

## When to Use
- A task requires newsletter writing before downstream steps can proceed safely.
- Ambiguity or missing evidence would change the outcome.
- The result must be recorded with reasons and evidence for later verification.

## Inputs / Outputs
| Area | Contract |
|---|---|
| Inputs | Task context, candidate inputs, and explicit acceptance criteria for newsletter writing. |
| Outputs | A decision or artifact with recorded reasons, rejected alternatives, and verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Define the goal, the constraints, and the boundary of what this procedure may change.
2. Inventory the available inputs and flag gaps or ambiguities that block progress.
3. Execute the newsletter writing steps in a bounded, checkpointed way.
4. Compare the actual outcome against the expected outcome and record deviations.
5. On failure, apply the declared fallback path, and never widen permissions to recover.
6. Emit a structured result with evidence and provenance for downstream consumers.

## Runnable Example
```python
# Newsletter Writing: deterministic check
def check_budget(estimate, limit):
    if estimate > limit:
        raise ValueError("estimate %s exceeds limit %s" % (estimate, limit))
    return "approved"

assert check_budget(3, 5) == "approved"
try:
    check_budget(7, 5)
    raise AssertionError("should have raised")
except ValueError:
    print("guard held")
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
Newsletter drafting is among the most requested 2026 content agent tasks. These are dated public signals, not adoption metrics.

## Related
- blog-writing.md
- copywriting.md
- social-media-post.md
