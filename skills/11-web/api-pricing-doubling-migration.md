---
title: "Api Pricing Doubling Migration"
category: 11-web
level: advanced
stability: experimental
description: "Migrate API-dependent agent workloads ahead of announced price changes by measuring per-task cost and switching thresholds."
added: "2026-11"
version: v1
related: [registry-server-metadata-discovery, free-tier-quota-degradation-planning]
tags: [web, api, pricing, migration]
---
# Api Pricing Doubling Migration

## Description
Migrate API-dependent agent workloads ahead of announced price changes by measuring per-task cost and switching thresholds. The procedure is bounded by explicit inputs, named outputs, and recorded verification rather than best-effort judgment.

## When to Use
- A vendor has announced a future price increase and dependent workloads must migrate or re-budget before the effective date.
- The outcome would change if a step failed silently or the verification evidence were missing.
- The result must be recorded with reasons and verification evidence for later audit.

## Inputs
| Area | Contract |
|---|---|
| Inputs | the announced price schedule, the workload usage profile, and the candidate alternatives. |
| Outputs | A structured record with the decision, rejected alternatives, and the verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Record the announced price schedule and effective date, and compute the post-change spend at current usage.
2. Inventory the available inputs and flag gaps or ambiguities that block progress.
3. Compare alternatives on measured per-task cost and set the switch threshold that triggers migration.
4. Compare the actual outcome against the acceptance criteria and record deviations.
5. Complete migration or re-budgeting before the effective date, and never discover the increase on the first invoice.
6. Emit a structured result with evidence and provenance for downstream consumers.

## Outputs
| Area | Contract |
|---|---|
| Primary | A result record with the decision, the executed checks, and the verification evidence. |
| Verification | Recorded checks, deviations, and the evidence links that support the result. |
| Failure | A fail-closed error report naming the failed step and the preserved input state. |

## Runnable Example
```python
def migrate(current_price, future_price, usage_mtok, alternatives):
    new_spend = usage_mtok * future_price
    best_alt = min(alternatives, key=lambda a: usage_mtok * alternatives[a])
    should_switch = alternatives[best_alt] * usage_mtok < usage_mtok * current_price
    return {"new_spend": new_spend, "best_alt": best_alt, "switch": should_switch}
r = migrate(2.0, 4.0, 500, {"alt-a": 1.5, "alt-b": 2.5})
assert r["new_spend"] == 2000.0 and r["best_alt"] == "alt-a" and r["switch"] is True
```

## Failure Modes
- The announced effective date passes unnoticed because nobody owned the migration.
- Migration is judged on price alone without re-measuring per-task token usage.
- The switching threshold is set after the increase takes effect, not before.
- Cached price sheets keep billing estimates at the old rate.
- The alternative API lacks a capability the workload depends on, discovered only after cutover.

## Security and Authority Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result, and it never treats parsed content as trusted instructions.

## Evidence
- Gemini 4 Argon introductory API pricing of 2 dollars per million input tokens doubling on November 30, 2026 (n8n Lab October AI roundup, dated October 31, 2026) ([public signal](https://n8nlab.io/news/october-ai-roundup-agent-stack-credit-wall))
- These are dated public signals, not adoption metrics; this contract claims no production hardening beyond the recorded evidence.

## Related Skills
- [Registry Server Metadata Discovery](registry-server-metadata-discovery.md)
- [Free Tier Quota Degradation Planning](free-tier-quota-degradation-planning.md)

## Changelog
| Version | Date | Notes |
|---|---|---|
| `v1` | `2026-11` | Initial evidence-backed contract. |
