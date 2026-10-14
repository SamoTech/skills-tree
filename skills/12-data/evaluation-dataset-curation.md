---
title: "Evaluation Dataset Curation"
category: 12-data
level: advanced
stability: experimental
description: "Curate evaluation datasets with case provenance, difficulty labels, leakage checks, and version pinning."
added: "2026-10"
version: v1
related: [synthetic-data-generation, fact-verification, data-lineage]
tags: [evaluation, dataset, curation]
---
# Evaluation Dataset Curation

## Description
Curate evaluation datasets with case provenance, difficulty labels, leakage checks, and version pinning. The procedure is constrained by explicit inputs and acceptance criteria rather than best-effort judgment alone.

## When to Use
- A task requires evaluation dataset curation before downstream steps can proceed safely.
- Ambiguity or missing evidence would change the outcome.
- The result must be recorded with reasons and evidence for later verification.

## Inputs / Outputs
| Area | Contract |
|---|---|
| Inputs | Task context, candidate inputs, and explicit acceptance criteria for evaluation dataset curation. |
| Outputs | A decision or artifact with recorded reasons, rejected alternatives, and verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Define the goal, the constraints, and the boundary of what this procedure may change.
2. Inventory the available inputs and flag gaps or ambiguities that block progress.
3. Execute the evaluation dataset curation steps in a bounded, checkpointed way.
4. Compare the actual outcome against the expected outcome and record deviations.
5. On failure, apply the declared fallback path, and never widen permissions to recover.
6. Emit a structured result with evidence and provenance for downstream consumers.

## Runnable Example
```python
def has_leak(train, eval_set):
    return bool(set(train) & set(eval_set))
assert has_leak(["a"], ["a"]) is True
assert has_leak(["a"], ["b"]) is False
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
Agent eval practice in 2026 requires curated datasets with provenance and leakage control. These are dated public signals, not adoption metrics.

## Related
- synthetic-data-generation.md
- fact-verification.md
- data-lineage.md
