---
title: "Retrieval Result Diversification"
category: 03-memory
level: advanced
stability: experimental
description: "Diversify retrieval results so near-duplicate passages do not dominate context, with explicit similarity thresholds and a recorded tradeoff against pure relevance."
added: "2026-10"
version: v1
related: [vector-store-retrieval, rag, retrieval-relevance-feedback]
tags: [retrieval, rag, diversity]
---

# Retrieval Result Diversification

## Description
Diversify retrieval results so near-duplicate passages do not dominate context, with explicit similarity thresholds and a recorded tradeoff against pure relevance. The procedure is constrained by explicit inputs and acceptance criteria rather than best-effort judgment alone.

## When to Use
- top-k retrieval returns near-identical passages and context is wasted before downstream steps can proceed safely.
- Ambiguity or missing evidence would change the outcome.
- The result must be recorded with reasons and evidence for later verification.

## Inputs / Outputs
| Area | Contract |
|---|---|
| Inputs | Task context, candidate inputs, and explicit acceptance criteria for retrieval result diversification work. |
| Outputs | A decision or artifact with recorded reasons, rejected alternatives, and verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Define the goal, the constraints, and the boundary of what this procedure may change.
2. Inventory the available inputs and flag gaps or ambiguities that block progress.
3. Execute the retrieval result diversification steps in a bounded, checkpointed way.
4. Compare the actual outcome against the expected outcome and record deviations.
5. On failure, apply the declared fallback path, and never widen permissions to recover.
6. Emit a structured result with evidence and provenance for downstream consumers.

## Runnable Example
```python
def diversify(items, k, max_sim=0.9):
    chosen = []
    for item in items:
        if len(chosen) >= k:
            break
        if all(sim(item, c) < max_sim for c in chosen):
            chosen.append(item)
    return chosen

def sim(a, b):
    return 1.0 if a["topic"] == b["topic"] else 0.0

items = [{"topic": "x"}, {"topic": "x"}, {"topic": "y"}]
assert diversify(items, 2) == [{"topic": "x"}, {"topic": "y"}]
```

## Failure Modes
- Diversifying so far that required duplicates are dropped.
- Hiding the relevance cost of diversification.
- Using a similarity threshold without calibration.
- Deduplicating exact text but not paraphrases.
- Ignoring ordering guarantees downstream code expects.

## Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result.

## Evidence
Context-efficiency techniques are a recurring 2026 RAG optimization topic in public coverage; this is a dated signal, not an adoption metric.

## Related
- vector-store-retrieval.md
- rag.md
- retrieval-relevance-feedback.md
