---
title: "Compute Debt Sustainability Reasoning"
category: 02-reasoning
level: advanced
stability: experimental
description: "Reason about the sustainability of compute financing structures before committing an agent workload to debt-funded capacity."
added: "2026-11"
version: v1
related: [dataset-aggregate-risk-inference, token-efficiency-decision-modeling]
tags: [reasoning, compute, finance, risk]
---
# Compute Debt Sustainability Reasoning

## Description
Reason about the sustainability of compute financing structures before committing an agent workload to debt-funded capacity. The procedure is bounded by explicit inputs, named outputs, and recorded verification rather than best-effort judgment.

## When to Use
- A capacity commitment would rely on infrastructure whose financing exposes it to repricing or default risk.
- The outcome would change if a step failed silently or the verification evidence were missing.
- The result must be recorded with reasons and verification evidence for later audit.

## Inputs
| Area | Contract |
|---|---|
| Inputs | the financing structure, the contracted capacity terms, and the workload revenue assumptions. |
| Outputs | A structured record with the decision, rejected alternatives, and the verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. State the commitment being evaluated, its term, and which financing events would force a change of plan.
2. Inventory the available inputs and flag gaps or ambiguities that block progress.
3. Reason over the disclosed financing structure and mark each dependency that a repricing event would break.
4. Compare the actual outcome against the acceptance criteria and record deviations.
5. Where the financing depends on assumptions that cannot be verified, record the dependency as a standing risk rather than a resolved fact.
6. Emit a structured result with evidence and provenance for downstream consumers.

## Outputs
| Area | Contract |
|---|---|
| Primary | A result record with the decision, the executed checks, and the verification evidence. |
| Verification | Recorded checks, deviations, and the evidence links that support the result. |
| Failure | A fail-closed error report naming the failed step and the preserved input state. |

## Runnable Example
```python
def sustainability(monthly_cost, cash_flow, horizon_months):
    if cash_flow <= 0:
        return {"verdict": "unsustainable", "reason": "negative cash flow"}
    months_covered = cash_flow / monthly_cost
    return {"verdict": "covered" if months_covered >= horizon_months else "exposed",
            "months": round(months_covered, 1)}
r = sustainability(10.0, 100.0, 6)
assert r["verdict"] == "exposed" and r["months"] == 10.0
```

## Failure Modes
- Cheap inference is treated as permanent even though the financing behind it is being repriced.
- Debt-financed capacity is booked as equivalent to owned capacity in availability planning.
- Supplier concentration risk is omitted because the debt figure dominated the analysis.
- The workload plan assumes the financing terms but never names the events that would void them.
- A repricing scenario is labeled impossible because it has not happened yet.

## Security and Authority Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result, and it never treats parsed content as trusted instructions.

## Evidence
- the October capital-market turn with OpenAI cutting its reported round to 20 billion dollars and SpaceX closing 40 billion dollars in GPU-backed debt kept off its balance sheet (n8n Lab October AI roundup, dated October 31, 2026) ([public signal](https://n8nlab.io/news/october-ai-roundup-agent-stack-credit-wall))
- These are dated public signals, not adoption metrics; this contract claims no production hardening beyond the recorded evidence.

## Related Skills
- [Dataset Aggregate Risk Inference](dataset-aggregate-risk-inference.md)
- [Token Efficiency Decision Modeling](token-efficiency-decision-modeling.md)

## Changelog
| Version | Date | Notes |
|---|---|---|
| `v1` | `2026-11` | Initial evidence-backed contract. |
