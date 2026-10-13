---
name: session-boundary-memory-merge
description: Merge memory accumulated across session boundaries with conflict detection, deduplicate near-identical entries, and preserve the provenance of merged facts.
metadata:
  source: skills/03-memory/session-boundary-memory-merge.md
  category: 03-memory
  version: "v1"
---

# Session Boundary Memory Merge

## Description
Merge memory accumulated across session boundaries with conflict detection, deduplicate near-identical entries, and preserve the provenance of merged facts. The procedure is constrained by explicit inputs and acceptance criteria rather than best-effort judgment alone.

## When to Use
- facts learned in separate sessions must be combined without losing or double-counting before downstream steps can proceed safely.
- Ambiguity or missing evidence would change the outcome.
- The result must be recorded with reasons and evidence for later verification.

## Inputs / Outputs
| Area | Contract |
|---|---|
| Inputs | Task context, candidate inputs, and explicit acceptance criteria for session boundary memory merge work. |
| Outputs | A decision or artifact with recorded reasons, rejected alternatives, and verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Define the goal, the constraints, and the boundary of what this procedure may change.
2. Inventory the available inputs and flag gaps or ambiguities that block progress.
3. Execute the session boundary memory merge steps in a bounded, checkpointed way.
4. Compare the actual outcome against the expected outcome and record deviations.
5. On failure, apply the declared fallback path, and never widen permissions to recover.
6. Emit a structured result with evidence and provenance for downstream consumers.

## Runnable Example
```python
def merge(batches):
    merged, conflicts = {}, []
    for batch in batches:
        for key, value in batch.items():
            if key in merged and merged[key] != value:
                conflicts.append(key)
            merged[key] = value
    return merged, conflicts

a, b = {"tz": "UTC", "theme": "dark"}, {"tz": "UTC", "theme": "light"}
merged, conflicts = merge([a, b])
assert merged["tz"] == "UTC" and conflicts == ["theme"]
```

## Failure Modes
- Overwriting newer facts with older ones.
- Resolving conflicts without recording either provenance.
- Duplicating entries that differ only in formatting.
- Losing session-scoped facts that should not merge.
- Silently picking the last write as the truth.

## Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result.

## Evidence
Cross-session continuity is a recurring 2026 agent-memory request signal in public issue discussion, including repository issue #87 on hierarchical memory; this is a dated signal, not an adoption metric.

## Related
- memory-conflict-resolution.md
- memory-consolidation.md
- cross-session-persistence.md
