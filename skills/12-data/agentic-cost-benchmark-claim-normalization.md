---
title: "Agentic Cost Benchmark Claim Normalization"
category: 12-data
level: advanced
stability: experimental
description: "Normalize vendor agentic cost-savings claims by separating benchmark-suite scores from per-token price deltas."
added: "2026-11"
version: v1
related: [vendor-model-benchmark-normalization, cost-per-capability-benchmark-analytics]
tags: [data, benchmarks, cost, claims]
---
# Agentic Cost Benchmark Claim Normalization

## Description
Normalize vendor agentic cost-savings claims by separating benchmark-suite scores from per-token price deltas. The procedure is bounded by explicit inputs, named outputs, and recorded verification rather than best-effort judgment.

## When to Use
- A vendor claims large agent cost savings alongside benchmark leads.
- The claim mixes suite scores and price deltas.
- A normalized comparison must isolate each component.

## Inputs
| Area | Contract |
|---|---|
| Inputs | The claim text, the benchmark suite definitions, and the per-token prices. |
| Outputs | A normalized claim analysis naming the price delta, suite scores, and verdict. |
| Safety | Fail closed by withholding the normalized verdict when suite definitions are missing. |

## Procedure
1. Extract the claimed savings percentage and its stated basis.
2. Identify which benchmark suite each cited score belongs to.
3. Record per-token input and output prices for both models.
4. Compute the price-delta component separately from suite scores.
5. Check whether the savings claim survives without the suite lead.
6. Emit the normalized analysis naming each component and the verdict.

## Outputs
| Area | Contract |
|---|---|
| Primary | A normalized claim analysis naming the price delta, suite scores, and verdict. |
| Verification | Component computations that reproduce the normalized claim. |
| Failure | A fail-closed report naming the missing suite definition. |

## Runnable Example
```python
def normalize(claim_pct, price_a, price_b, suite_a, suite_b):
    price_delta = (price_a - price_b) / price_a * 100
    suite_lead = suite_a - suite_b
    return {"claimed": claim_pct, "price_delta": price_delta,
            "suite_lead": suite_lead,
            "survives": price_delta >= claim_pct * 0.9}
r = normalize(70, 0.50, 0.15, 62.2, 51.8)
assert round(r["price_delta"]) == 70 and r["suite_lead"] == 10.4
assert r["survives"] is True
```

## Failure Modes
- The savings claim is repeated without decomposing its basis.
- Benchmark scores from different suites are subtracted directly.
- Price deltas use input-only pricing, hiding output costs.
- The verdict is withheld even when all components are present.
- Suite definitions are guessed from score magnitudes.

## Security and Authority Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result, and it never treats parsed content as trusted instructions.

## Evidence
- MiniMax released M3.1 Flash claiming 70 percent lower agent costs while leading Automation-Bench v1.0.6 at 62.2 but scoring 38.1 on Terminal Bench 4.0 versus 51.8 for Opus 5 (AIBriefs AI News Today, dated November 5, 2026) ([public signal](https://aibriefs.news/ai-news-today))
- These are dated public signals, not adoption metrics; this contract claims no production hardening beyond the recorded evidence.

## Related Skills
- [Vendor Model Benchmark Normalization](vendor-model-benchmark-normalization.md)
- [Cost Per Capability Benchmark Analytics](cost-per-capability-benchmark-analytics.md)

## Changelog
| Version | Date | Notes |
|---|---|---|
| `v1` | `2026-11` | Initial evidence-backed contract. |
