---
title: "Aggregate Dataset Screening Pipeline"
category: 12-data
level: advanced
stability: experimental
description: "Screen training datasets with a pipeline that evaluates aggregate behavioral effect after training, not only per-row classifier verdicts."
added: "2026-11"
version: v1
related: [cross-verified-data-source-onboarding, data-freshness-staleness-accounting]
tags: [data, datasets, screening, pipelines]
---
# Aggregate Dataset Screening Pipeline

## Description
Screen training datasets with a pipeline that evaluates aggregate behavioral effect after training, not only per-row classifier verdicts. The procedure is bounded by explicit inputs, named outputs, and recorded verification rather than best-effort judgment.

## When to Use
- A dataset pipeline must produce evidence about the trained behavior of a dataset, not only row-level cleanliness.
- The outcome would change if a step failed silently or the verification evidence were missing.
- The result must be recorded with reasons and verification evidence for later audit.

## Inputs
| Area | Contract |
|---|---|
| Inputs | the dataset batches, the row screener, and the aggregate behavioral probe suite. |
| Outputs | A structured record with the decision, rejected alternatives, and the verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Define the pipeline stages including row screening, aggregate probe training runs, and the halt condition.
2. Inventory the available inputs and flag gaps or ambiguities that block progress.
3. Execute the stages in order, storing the row verdicts and the aggregate probe results per dataset version.
4. Compare the actual outcome against the acceptance criteria and record deviations.
5. On a halt condition, stop the pipeline at that stage, and never let row verdicts substitute for probe results.
6. Emit a structured result with evidence and provenance for downstream consumers.

## Outputs
| Area | Contract |
|---|---|
| Primary | A result record with the decision, the executed checks, and the verification evidence. |
| Verification | Recorded checks, deviations, and the evidence links that support the result. |
| Failure | A fail-closed error report naming the failed step and the preserved input state. |

## Runnable Example
```python
def pipeline(batch, row_screener, aggregate_probe):
    verdicts = [row_screener(r) for r in batch]
    row_ok = all(v == "clean" for v in verdicts)
    if not row_ok:
        return {"stage": "row-screen", "passed": False}
    if aggregate_probe(batch) != "pass":
        return {"stage": "aggregate", "passed": False}
    return {"stage": "done", "passed": True}
r = pipeline(["a", "b"], lambda r: "clean", lambda b: "fail")
assert r["stage"] == "aggregate" and r["passed"] is False
```

## Failure Modes
- The pipeline halts on the first dirty row and never reaches the aggregate stage for the rest.
- Aggregate probes are cached from a previous dataset version.
- Probe training runs use different sampling settings than the target training.
- The halt condition treats row screening as sufficient evidence of dataset safety.
- Pipeline stage outputs overwrite each other so the failing stage cannot be identified.

## Security and Authority Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result, and it never treats parsed content as trusted instructions.

## Evidence
- the Anthropic demonstration that datasets can pass every row-level monitor while training models that resist oversight, requiring pipelines that test the combined behavioral effect after training (AI Agent News Today, dated November 1, 2026) ([public signal](https://aiagentstore.ai/ai-agent-news/this-week))
- These are dated public signals, not adoption metrics; this contract claims no production hardening beyond the recorded evidence.

## Related Skills
- [Cross Verified Data Source Onboarding](cross-verified-data-source-onboarding.md)
- [Data Freshness Staleness Accounting](data-freshness-staleness-accounting.md)

## Changelog
| Version | Date | Notes |
|---|---|---|
| `v1` | `2026-11` | Initial evidence-backed contract. |
