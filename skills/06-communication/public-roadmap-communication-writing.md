---
title: "Public Roadmap Communication Writing"
category: 06-communication
level: advanced
stability: experimental
description: "Write public roadmap updates that state shipped items, committed next steps, and honest unknowns without overpromising."
added: "2026-10"
version: v1
related: [release-notes-generation, community-response-drafting, changelog-writing]
tags: [public, roadmap, communication, writing]
---
# Public Roadmap Communication Writing

## Description
Write public roadmap updates that state shipped items, committed next steps, and honest unknowns without overpromising. The procedure is constrained by explicit inputs and acceptance criteria rather than best-effort judgment alone.

## When to Use
- A task requires public roadmap communication writing before downstream steps can proceed safely.
- Ambiguity or missing evidence would change the outcome.
- The result must be recorded with reasons and evidence for later verification.

## Inputs / Outputs
| Area | Contract |
|---|---|
| Inputs | Task context, candidate inputs, and explicit acceptance criteria for public roadmap communication writing. |
| Outputs | A decision or artifact with recorded reasons, rejected alternatives, and verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Define the goal, the constraints, and the boundary of what this procedure may change.
2. Inventory the available inputs and flag gaps or ambiguities that block progress.
3. Execute the public roadmap communication writing steps in a bounded, checkpointed way.
4. Compare the actual outcome against the expected outcome and record deviations.
5. On failure, apply the declared fallback path, and never widen permissions to recover.
6. Emit a structured result with evidence and provenance for downstream consumers.

## Runnable Example
```python
def roadmap(shipped, planned):
    return {"shipped": shipped, "planned": planned, "not_committed": []}
r = roadmap(["search"], ["export"])
assert r["shipped"] == ["search"]
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
Public roadmap communication is a recurring request in open-source project stewardship discussions in 2026. These are dated public signals, not adoption metrics.

## Related
- release-notes-generation.md
- community-response-drafting.md
- changelog-writing.md
