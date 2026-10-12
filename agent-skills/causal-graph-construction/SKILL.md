---
name: causal-graph-construction
description: Build an explicit causal graph from observed events and stated mechanisms, distinguishing correlation from causation before using the graph for intervention decisions.
metadata:
  source: skills/02-reasoning/causal-graph-construction.md
  category: 02-reasoning
  version: "v1"
---

# Causal Graph Construction

## Description
Build an explicit causal graph from observed events and stated mechanisms, distinguishing correlation from causation before using the graph for intervention decisions. The procedure is constrained by explicit inputs and acceptance criteria rather than best-effort judgment alone.

## When to Use
- Multiple inputs or candidates compete and must be resolved by explicit criteria.
- A wrong intermediate result would propagate into consequential actions.
- The task repeats and benefits from a deterministic procedure.

## Inputs / Outputs
| Area | Contract |
|---|---|
| Inputs | Task context, candidate inputs, and explicit acceptance criteria for causal graph construction. |
| Outputs | A decision or artifact with recorded reasons, rejected alternatives, and verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Define the goal, the constraints, and the boundary of what this procedure may change.
2. Inventory the available inputs and flag gaps or ambiguities that block progress.
3. Execute the causal graph construction steps in a bounded, checkpointed way.
4. Compare the actual outcome against the expected outcome and record deviations.
5. On failure, apply the declared fallback path, and never widen permissions to recover.
6. Emit a structured result with evidence and provenance for downstream consumers.

## Runnable Example
```python
# Causal Graph Construction: deterministic check
attempts = []
def flaky(n):
    attempts.append(n)
    return n >= 3

tries, max_tries, done = 0, 5, False
while tries < max_tries:
    tries += 1
    if flaky(tries):
        done = True
        break
assert done and tries == 3
print("succeeded after", tries, "attempts")
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
2026 agent research on intervention and explanation requests explicit causal models rather than correlational summaries. These are dated public signals, not adoption metrics.

## Related
- causal.md
- root-cause-analysis.md
- counterfactual-reasoning.md
