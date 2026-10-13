---
name: search-federation-tooling
description: Federate searches across multiple providers with per-provider timeouts, result merging rules, and provenance on every returned item.
metadata:
  source: skills/07-tool-use/search-federation-tooling.md
  category: 07-tool-use
  version: "v1"
---

# Search Federation Tooling

## Description
Federate searches across multiple providers with per-provider timeouts, result merging rules, and provenance on every returned item. The procedure is constrained by explicit inputs and acceptance criteria rather than best-effort judgment alone.

## When to Use
- a search tool must combine several providers without losing provenance or hanging on one slow source.
- Ambiguity or missing evidence would change the outcome.
- The result must be recorded with reasons and evidence for later verification.

## Inputs / Outputs
| Area | Contract |
|---|---|
| Inputs | Task context, candidate inputs, and explicit acceptance criteria for search federation tooling work. |
| Outputs | A decision or artifact with recorded reasons, rejected alternatives, and verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Define the goal, the constraints, and the boundary of what this procedure may change.
2. Inventory the available inputs and flag gaps or ambiguities that block progress.
3. Execute the search federation tooling steps in a bounded, checkpointed way.
4. Compare the actual outcome against the expected outcome and record deviations.
5. On failure, apply the declared fallback path, and never widen permissions to recover.
6. Emit a structured result with evidence and provenance for downstream consumers.

## Runnable Example
```python
def merge(providers, timeout_budget):
    usable = [p for p in providers if p["latency"] <= timeout_budget]
    ranked = sorted(usable, key=lambda p: -p["score"])
    return [(r["provider"], r["id"]) for p in ranked for r in p["results"][:2]]

ps = [
    {"provider": "a", "latency": 50, "score": 0.9, "results": [{"id": "1"}]},
    {"provider": "b", "latency": 900, "score": 0.99, "results": [{"id": "2"}]},
]
out = merge(ps, 100)
assert ("a", "1") in out and all(p != "b" for p, _ in out)
```

## Failure Modes
- One slow provider blocking the whole call.
- Merging without provider labels so sources are lost.
- No timeout so the tool hangs indefinitely.
- Ranking by provider bias instead of relevance.
- Silently dropping provider errors from the result.

## Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result.

## Evidence
Search federation across providers is a recurring 2026 agent-tooling request in public discussion; this is a dated signal, not an adoption metric.

## Related
- web-search.md
- multi-provider-redundancy.md
- api-pagination.md
