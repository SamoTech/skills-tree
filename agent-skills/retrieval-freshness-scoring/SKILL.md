---
name: retrieval-freshness-scoring
description: Score retrieved items by age and source update cadence, surface staleness alongside relevance, and refuse to present stale evidence as current.
metadata:
  source: skills/03-memory/retrieval-freshness-scoring.md
  category: 03-memory
  version: "v1"
---

# Retrieval Freshness Scoring

## Description
Score retrieved items by age and source update cadence, surface staleness alongside relevance, and refuse to present stale evidence as current. The procedure is constrained by explicit inputs and acceptance criteria rather than best-effort judgment alone.

## When to Use
- answers depend on evidence that may be outdated before downstream steps can proceed safely.
- Ambiguity or missing evidence would change the outcome.
- The result must be recorded with reasons and evidence for later verification.

## Inputs / Outputs
| Area | Contract |
|---|---|
| Inputs | Task context, candidate inputs, and explicit acceptance criteria for retrieval freshness scoring work. |
| Outputs | A decision or artifact with recorded reasons, rejected alternatives, and verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Define the goal, the constraints, and the boundary of what this procedure may change.
2. Inventory the available inputs and flag gaps or ambiguities that block progress.
3. Execute the retrieval freshness scoring steps in a bounded, checkpointed way.
4. Compare the actual outcome against the expected outcome and record deviations.
5. On failure, apply the declared fallback path, and never widen permissions to recover.
6. Emit a structured result with evidence and provenance for downstream consumers.

## Runnable Example
```python
def freshness(ts, now, half_life_days=30.0):
    age_days = max(0.0, (now - ts) / 86400.0)
    return 0.5 ** (age_days / half_life_days)

now = 86400 * 30
assert abs(freshness(now - 86400 * 30, now) - 0.5) < 1e-9
assert freshness(now, now) == 1.0
assert freshness(now - 86400 * 400, now) < 0.01
```

## Failure Modes
- Ranking by relevance only and hiding age.
- Using one decay rate for sources with different cadences.
- Presenting a stale snapshot as the live state.
- Refreshing scores without re-fetching content.
- Ignoring the source last-modified header when present.

## Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result.

## Evidence
Content freshness for agent answers is a recurring 2026 request as agents cite live web sources; this is a dated signal, not an adoption metric.

## Related
- retrieval-relevance-feedback.md
- rag.md
- memory-ttl.md
