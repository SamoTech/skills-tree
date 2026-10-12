---
name: retrieval-prefetching
description: Predict which memories or documents a task will need and prefetch them before they are requested, with a measured hit-rate target and a fallback on miss.
metadata:
  source: skills/03-memory/retrieval-prefetching.md
  category: 03-memory
  version: "v1"
---
# Retrieval Prefetching

## Description
Predict which memories or documents a task will need and prefetch them before they are requested, with a measured hit-rate target and a fallback on miss. The procedure is constrained by explicit inputs and acceptance criteria rather than best-effort judgment alone.

## When to Use
- A task requires retrieval prefetching before downstream steps can proceed safely.
- Ambiguity or missing evidence would change the outcome.
- The result must be recorded with reasons and evidence for later verification.

## Inputs / Outputs
| Area | Contract |
|---|---|
| Inputs | Task context, candidate inputs, and explicit acceptance criteria for retrieval prefetching. |
| Outputs | A decision or artifact with recorded reasons, rejected alternatives, and verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Define the goal, the constraints, and the boundary of what this procedure may change.
2. Inventory the available inputs and flag gaps or ambiguities that block progress.
3. Execute the retrieval prefetching steps in a bounded, checkpointed way.
4. Compare the actual outcome against the expected outcome and record deviations.
5. On failure, apply the declared fallback path, and never widen permissions to recover.
6. Emit a structured result with evidence and provenance for downstream consumers.

## Runnable Example
```python
# Retrieval Prefetching: deterministic check
allowed = {"idle": {"running"}, "running": {"done", "failed"}, "failed": {"idle"}}

def transition(state, nxt):
    return nxt in allowed.get(state, set())

assert transition("idle", "running")
assert not transition("idle", "done")
print("transitions checked")
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
Latency-bounded agent serving is a 2026 production theme; prefetching appears in published RAG serving optimizations. These are dated public signals, not adoption metrics.

## Related
- vector-store-retrieval.md
- memory-indexing.md
- rag.md
