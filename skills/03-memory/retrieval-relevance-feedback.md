---
title: "Retrieval Relevance Feedback"
category: 03-memory
level: basic
stability: experimental
description: "Feed explicit relevance judgments from downstream use back into retrieval parameters such as thresholds and ranking weights, with measured before-and-after evaluation."
added: "2026-10"
version: v1
related: [rag, vector-store-retrieval, memory-indexing]
tags: [retrieval, relevance, feedback, memory]
---

# Retrieval Relevance Feedback

## Description
Feed explicit relevance judgments from downstream use back into retrieval parameters such as thresholds and ranking weights, with measured before-and-after evaluation. The procedure is constrained by explicit inputs and acceptance criteria rather than best-effort judgment alone.

## When to Use
- The task has explicit constraints such as time, budget, or safety that must gate the outcome.
- A silent failure mode exists that must be surfaced rather than swallowed.
- Verification evidence is required before the result is trusted.

## Inputs / Outputs
| Area | Contract |
|---|---|
| Inputs | Task context, candidate inputs, and explicit acceptance criteria for retrieval relevance feedback. |
| Outputs | A decision or artifact with recorded reasons, rejected alternatives, and verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Normalize the task into explicit inputs, constraints, and acceptance criteria.
2. Gather the required evidence and check completeness before proceeding.
3. Apply the retrieval relevance feedback procedure using the declared criteria only.
4. Record the outcome, rejected alternatives, and the reason for each rejection.
5. Verify the result against the acceptance criteria with an independent check.
6. Report the result with evidence, and escalate explicitly when a criterion cannot be met.

## Runnable Example
```python
# Retrieval Relevance Feedback: deterministic check
allowed = {"idle": {"running"}, "running": {"done", "failed"}, "failed": {"idle"}}

def transition(state, nxt):
    return nxt in allowed.get(state, set())

assert transition("idle", "running")
assert not transition("idle", "done")
print("transitions checked")
```

## Failure Modes
- Proceeding with retrieval relevance feedback without the required evidence or inputs.
- Treating an unverified result as verified.
- Silently swallowing errors instead of failing closed with reasons.
- Optimizing the stated metric while violating the stated constraint.
- Losing the audit trail of decisions and rejected alternatives.

## Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result.

## Evidence
RAG quality-improvement requests recur across 2026 public threads; feedback-driven retrieval tuning is published in agent RAG guides. These are dated public signals, not adoption metrics.

## Related
- rag.md
- vector-store-retrieval.md
- memory-indexing.md
