---
title: "Creative Brief Decomposition"
category: 13-creative
level: advanced
stability: experimental
description: "Decompose a creative brief into concrete generation tasks with constraints, references, and acceptance criteria."
added: "2026-10"
version: v1
related: [creative-writing, copywriting, storyboard-generation]
tags: [creative, brief, decomposition]
---
# Creative Brief Decomposition

## Description
Decompose a creative brief into concrete generation tasks with constraints, references, and acceptance criteria. The procedure is constrained by explicit inputs and acceptance criteria rather than best-effort judgment alone.

## When to Use
- A task requires creative brief decomposition before downstream steps can proceed safely.
- Ambiguity or missing evidence would change the outcome.
- The result must be recorded with reasons and evidence for later verification.

## Inputs / Outputs
| Area | Contract |
|---|---|
| Inputs | Task context, candidate inputs, and explicit acceptance criteria for creative brief decomposition. |
| Outputs | A decision or artifact with recorded reasons, rejected alternatives, and verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Define the goal, the constraints, and the boundary of what this procedure may change.
2. Inventory the available inputs and flag gaps or ambiguities that block progress.
3. Execute the creative brief decomposition steps in a bounded, checkpointed way.
4. Compare the actual outcome against the expected outcome and record deviations.
5. On failure, apply the declared fallback path, and never widen permissions to recover.
6. Emit a structured result with evidence and provenance for downstream consumers.

## Runnable Example
```python
def decompose(brief):
    tasks = [k for k in brief if brief[k]]
    return sorted(tasks)
assert decompose({"audience": "devs", "format": "", "tone": "plain"}) == ["audience", "tone"]
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
Creative-agent users request briefs turned into executable generation task lists in 2026 workflows. These are dated public signals, not adoption metrics.

## Related
- creative-writing.md
- copywriting.md
- storyboard-generation.md
