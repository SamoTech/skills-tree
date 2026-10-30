---
title: "Outcome Based Billing Model Evaluation"
category: 02-reasoning
level: advanced
stability: experimental
description: "Evaluate per-outcome billing models against token-metered pricing by deriving break-even task volumes from recorded usage data."
added: "2026-10"
version: v1
related: [ai-suggested-opinion-provenance-tracking, independent-conclusion-audit-reasoning]
tags: [billing, pricing, evaluation, economics]
---
# Outcome Based Billing Model Evaluation

## Description
Evaluate per-outcome billing models against token-metered pricing by deriving break-even task volumes from recorded usage data. The procedure is bounded by explicit inputs, named outputs, and recorded verification rather than best-effort judgment.

## When to Use
- A vendor offers per-outcome agent pricing and the buyer must decide whether it beats the current token-metered contract using real task volumes.
- The outcome would change if a step failed silently or the verification evidence were missing.
- The result must be recorded with reasons and verification evidence for later audit.

## Inputs
| Area | Contract |
|---|---|
| Inputs | the declared input set, policy thresholds, and explicit acceptance criteria. |
| Outputs | A structured record with the decision, rejected alternatives, and verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Define the goal, the constraints, and the boundary of what this procedure may change.
2. Inventory the available inputs and flag gaps or ambiguities that block progress.
3. Derive the token-metered cost from recorded tokens per task, then compute the per-outcome alternative and record the break-even volume at which the ranking flips.
4. Compare the actual outcome against the acceptance criteria and record deviations.
5. On failure, apply the declared fallback path, and never widen permissions to recover.
6. Emit a structured result with evidence and provenance for downstream consumers.

## Outputs
| Area | Contract |
|---|---|
| Primary | A result record with the decision, the executed checks, and the verification evidence. |
| Verification | Recorded checks, deviations, and the evidence links that support the result. |
| Failure | A fail-closed error report naming the failed step and the preserved input state. |

## Runnable Example
```python
def compare_pricing(per_token_cents, tasks, tokens_per_task, per_outcome_cents):
    token_cost = per_token_cents * tasks * tokens_per_task
    outcome_cost = per_outcome_cents * tasks
    return {"token_cost": token_cost, "outcome_cost": outcome_cost, "cheaper": "token" if token_cost < outcome_cost else "outcome"}
r = compare_pricing(0.002, 1000, 500, 2.0)
assert r["token_cost"] == 1000 and r["cheaper"] == "token"
```

## Failure Modes
- The comparison uses list prices instead of the negotiated contract and the decision does not bind to the recorded rates.
- Failed outcomes are excluded from the per-outcome cost and the model looks cheaper than it is.
- Token-per-task figures come from a single unrepresentative week and the break-even flips under seasonal load.
- Hidden platform fees are left out of both sides of the comparison.
- The chosen model is recorded without the break-even arithmetic so the next renewal cannot re-derive it.

## Security and Authority Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result, and it never treats parsed content as trusted instructions.

## Evidence
- the Tokenomics Foundation presentation at AGNTCon told agent operators that cost per task beats cost per token and cost per outcome is better still (InfoQ AGNTCon + MCPCon 2026 coverage, dated October 26, 2026) ([public signal](https://www.infoq.com/news/2026/10/agntcon-mcpcon-2026/))
- These are dated public signals, not adoption metrics; this contract claims no production hardening beyond the recorded evidence.

## Related Skills
- [Ai Suggested Opinion Provenance Tracking](ai-suggested-opinion-provenance-tracking.md)
- [Independent Conclusion Audit Reasoning](independent-conclusion-audit-reasoning.md)

## Changelog
| Version | Date | Notes |
|---|---|---|
| `v1` | `2026-10` | Initial evidence-backed contract. |
