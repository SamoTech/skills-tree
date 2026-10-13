---
name: inter-annotator-agreement-measurement
description: Measure agreement between annotators with chance-corrected statistics and resolve disagreements through a recorded adjudication rule.
metadata:
  source: skills/12-data/inter-annotator-agreement-measurement.md
  category: 12-data
  version: "v1"
---

# Inter-Annotator Agreement Measurement

## Description
Measure agreement between annotators with chance-corrected statistics and resolve disagreements through a recorded adjudication rule. The procedure is constrained by explicit inputs and acceptance criteria rather than best-effort judgment alone.

## When to Use
- label quality must be quantified before a dataset is trusted.
- Ambiguity or missing evidence would change the outcome.
- The result must be recorded with reasons and evidence for later verification.

## Inputs / Outputs
| Area | Contract |
|---|---|
| Inputs | Task context, candidate inputs, and explicit acceptance criteria for inter-annotator agreement measurement work. |
| Outputs | A decision or artifact with recorded reasons, rejected alternatives, and verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Define the goal, the constraints, and the boundary of what this procedure may change.
2. Inventory the available inputs and flag gaps or ambiguities that block progress.
3. Execute the inter-annotator agreement measurement steps in a bounded, checkpointed way.
4. Compare the actual outcome against the expected outcome and record deviations.
5. On failure, apply the declared fallback path, and never widen permissions to recover.
6. Emit a structured result with evidence and provenance for downstream consumers.

## Runnable Example
```python
def observed_agreement(labels_a, labels_b):
    if len(labels_a) != len(labels_b):
        raise ValueError('label counts differ')
    return sum(a == b for a, b in zip(labels_a, labels_b)) / len(labels_a)

assert observed_agreement(['x', 'y'], ['x', 'y']) == 1.0
assert observed_agreement(['x', 'y'], ['y', 'y']) == 0.5
```

## Failure Modes
- Reporting raw agreement that ignores chance agreement.
- Adjudicating disagreements without recording the rule used.
- Comparing annotators who labeled different items.
- Publishing a dataset whose agreement was never measured.
- Hiding systematic disagreement between one pair of annotators.

## Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result.

## Evidence
Agreement measurement for labeling workforces recurs in 2026 dataset-quality requests; this is a dated signal, not an adoption metric.

## Related
- data-quality-scoring.md
- statistical-analysis.md
- data-profiling.md
