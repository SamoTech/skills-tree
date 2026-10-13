---
name: call-graph-construction
description: Build a static call graph of a codebase and use it to scope change impact before editing shared functions.
metadata:
  source: skills/05-code/call-graph-construction.md
  category: 05-code
  version: "v1"
---

# Call Graph Construction

## Description
Build a static call graph of a codebase and use it to scope change impact before editing shared functions. The procedure is constrained by explicit inputs and acceptance criteria rather than best-effort judgment alone.

## When to Use
- a shared function must change and the blast radius must be known before the edit starts.
- Ambiguity or missing evidence would change the outcome.
- The result must be recorded with reasons and evidence for later verification.

## Inputs / Outputs
| Area | Contract |
|---|---|
| Inputs | Task context, candidate inputs, and explicit acceptance criteria for call graph construction work. |
| Outputs | A decision or artifact with recorded reasons, rejected alternatives, and verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Define the goal, the constraints, and the boundary of what this procedure may change.
2. Inventory the available inputs and flag gaps or ambiguities that block progress.
3. Execute the call graph construction steps in a bounded, checkpointed way.
4. Compare the actual outcome against the expected outcome and record deviations.
5. On failure, apply the declared fallback path, and never widen permissions to recover.
6. Emit a structured result with evidence and provenance for downstream consumers.

## Runnable Example
```python
def impact(graph, start):
    seen, stack = set(), [start]
    while stack:
        n = stack.pop()
        if n in seen:
            continue
        seen.add(n)
        stack.extend(graph.get(n, []))
    return seen

graph = {"a": ["b"], "b": ["c"], "c": []}
assert impact(graph, "a") == {"a", "b", "c"}
assert impact(graph, "b") == {"b", "c"}
```

## Failure Modes
- Editing a hub function without its caller list.
- Trusting a dynamic-dispatch-unaware graph as complete.
- Building the graph on stale code without re-running.
- Confusing runtime profile edges with static edges.
- Skipping the graph for a small-looking change.

## Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result.

## Evidence
Change-impact scoping is a recurring 2026 request as agent edits touch shared code more often in public discussion; this is a dated signal, not an adoption metric.

## Related
- code-search.md
- monorepo-navigation.md
- static-analysis.md
