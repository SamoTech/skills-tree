---
name: small-model-tool-routing
description: Route tool calls between small and large models by call complexity, with fallback to the large model whenever confidence criteria are not met.
metadata:
  source: skills/07-tool-use/small-model-tool-routing.md
  category: 07-tool-use
  version: "v1"
---

# Small Model Tool Routing

## Description
Route tool calls between small and large models by call complexity, with fallback to the large model whenever confidence criteria are not met. The procedure is constrained by explicit inputs and acceptance criteria rather than best-effort judgment alone.

## When to Use
- tool calls should run on cheaper models when the call is simple and escalate when it is not.
- Ambiguity or missing evidence would change the outcome.
- The result must be recorded with reasons and evidence for later verification.

## Inputs / Outputs
| Area | Contract |
|---|---|
| Inputs | Task context, candidate inputs, and explicit acceptance criteria for small model tool routing work. |
| Outputs | A decision or artifact with recorded reasons, rejected alternatives, and verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Define the goal, the constraints, and the boundary of what this procedure may change.
2. Inventory the available inputs and flag gaps or ambiguities that block progress.
3. Execute the small model tool routing steps in a bounded, checkpointed way.
4. Compare the actual outcome against the expected outcome and record deviations.
5. On failure, apply the declared fallback path, and never widen permissions to recover.
6. Emit a structured result with evidence and provenance for downstream consumers.

## Runnable Example
```python
def route(call, threshold):
    if call["schema_depth"] <= threshold and not call["has_ambiguity"]:
        return "small"
    return "large"

assert route({"schema_depth": 2, "has_ambiguity": False}, 3) == "small"
assert route({"schema_depth": 2, "has_ambiguity": True}, 3) == "large"
```

## Failure Modes
- Routing on token count alone.
- No failure detection when the small model errs.
- Routing sensitive calls to the cheapest endpoint.
- No latency accounting for the routing decision itself.
- Never re-measuring the threshold after model updates.

## Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result.

## Evidence
Small-model routing for cost reduction is a documented 2026 inference-cost practice in public coverage; this is a dated signal, not an adoption metric.

## Related
- multi-provider-redundancy.md
- tool-token-budget-management.md
- tool-latency-probing.md
