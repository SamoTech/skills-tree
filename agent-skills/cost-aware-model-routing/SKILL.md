---
name: cost-aware-model-routing
description: Select an eligible model using task quality requirements, measured capability, latency constraints, and observed cost rather than defaulting every task to the most expensive model.
metadata:
  source: skills/15-orchestration/cost-aware-model-routing.md
  category: 15-orchestration
  version: "v1"
---

# Cost-Aware Model Routing

## Description
Route a task to the least-cost eligible model that satisfies quality, capability, latency, context, tool-use, and reliability constraints. Cost-aware routing is constrained optimization, not unconditional selection of the cheapest model.

## When to Use
- Multiple models can satisfy the same task.
- Model cost or latency materially affects runtime economics.
- A workload has measurable quality requirements and fallback models.
- Agent execution needs explicit routing and fallback policy.

## Inputs / Outputs
| Area | Contract |
|---|---|
| Inputs | Task requirements, candidate models, capability evidence, context/tool constraints, observed quality, latency, and current pricing/cost telemetry. |
| Outputs | Selected model, rejected candidates with reasons, routing evidence, and fallback policy. |
| Safety | A cheaper model must never bypass capability, security, or authorization requirements. |

## Procedure
1. Translate the task into hard requirements and measurable quality thresholds.
2. Remove models lacking required capability, context, tool, safety, or availability constraints.
3. Compare eligible models using measured quality, latency, and observed cost.
4. Select the least-cost model that satisfies hard requirements.
5. Preserve a deterministic fallback policy for timeout, quota, or quality failure.
6. Measure actual outcome and cost; update routing evidence only from observed results.

## Runnable Example
```python
models = [{"name": "small", "quality": 0.91, "cost": 1.0}, {"name": "large", "quality": 0.98, "cost": 4.0}]
eligible = [m for m in models if m["quality"] >= 0.90]
selected = min(eligible, key=lambda m: m["cost"])
assert selected["name"] == "small"
print(selected)
```

## Failure Modes
- Choosing a cheap but incapable model.
- Using stale or guessed pricing.
- Optimizing average cost while violating tail-latency or quality constraints.
- Routing sensitive work to a model without required security controls.
- Retrying across models without preserving task state or evidence.

## Boundary
Routing selects among already-authorized models. It does not grant model access, change data permissions, or weaken safety policy.

## Evidence
Public 2026 ecosystem work requests multi-model routing and cost optimization, including MCP inference routing and cost-aware LLM gateways. These signals support the capability gap but do not constitute adoption metrics.

## Related
- specialist-agent-routing.md
- retry-backoff.md
- capability-based-skill-selection.md
- budget-management.md
