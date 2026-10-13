---
name: embedding-drift-detection
description: Monitor embedding distributions for drift after model or corpus changes, alert when drift exceeds a declared threshold, and avoid silent retrieval degradation.
metadata:
  source: skills/03-memory/embedding-drift-detection.md
  category: 03-memory
  version: "v1"
---

# Embedding Drift Detection

## Description
Monitor embedding distributions for drift after model or corpus changes, alert when drift exceeds a declared threshold, and avoid silent retrieval degradation. The procedure is constrained by explicit inputs and acceptance criteria rather than best-effort judgment alone.

## When to Use
- embeddings changed after a model or corpus update and retrieval quality must be re-checked before downstream steps can proceed safely.
- Ambiguity or missing evidence would change the outcome.
- The result must be recorded with reasons and evidence for later verification.

## Inputs / Outputs
| Area | Contract |
|---|---|
| Inputs | Task context, candidate inputs, and explicit acceptance criteria for embedding drift detection work. |
| Outputs | A decision or artifact with recorded reasons, rejected alternatives, and verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Define the goal, the constraints, and the boundary of what this procedure may change.
2. Inventory the available inputs and flag gaps or ambiguities that block progress.
3. Execute the embedding drift detection steps in a bounded, checkpointed way.
4. Compare the actual outcome against the expected outcome and record deviations.
5. On failure, apply the declared fallback path, and never widen permissions to recover.
6. Emit a structured result with evidence and provenance for downstream consumers.

## Runnable Example
```python
def drift(old_centroid, new_centroid):
    return sum((a - b) ** 2 for a, b in zip(old_centroid, new_centroid)) ** 0.5

def alert_if(drift_value, threshold=0.3):
    return drift_value > threshold

old = [0.1, 0.2]
assert abs(drift(old, [0.1, 0.2])) < 1e-9
assert alert_if(drift(old, [0.9, 0.9])) is True
assert alert_if(drift(old, [0.12, 0.22])) is False
```

## Failure Modes
- Swapping embedding models without re-embedding the corpus.
- Alerting on drift without a declared threshold.
- Confusing corpus growth with distribution drift.
- Ignoring drift in query-time embeddings only.
- Letting retrieval silently degrade while alerts are postponed.

## Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result.

## Evidence
Embedding model churn is a recurring 2026 retrieval-pipeline concern in public coverage; this is a dated signal, not an adoption metric.

## Related
- embedding-generation.md
- embedding-model-selection.md
- memory-quality-auditing.md
