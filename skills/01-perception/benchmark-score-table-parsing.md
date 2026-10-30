---
title: "Benchmark Score Table Parsing"
category: 01-perception
level: advanced
stability: experimental
description: "Parse public benchmark score tables into comparable per-model records so that agents ground model-selection claims in cited numbers."
added: "2026-10"
version: v1
related: [complexity-claim-verification-reasoning, model-release-ledger-maintenance]
tags: [benchmarks, parsing, tables, scores]
---
# Benchmark Score Table Parsing

## Description
Parse public benchmark score tables into comparable per-model records so that agents ground model-selection claims in cited numbers. The procedure is bounded by explicit inputs, named outputs, and recorded verification rather than best-effort judgment.

## When to Use
- An agent reads a published benchmark table and must produce normalized records that keep model, benchmark, and score bound together.
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
3. Extract rows into normalized records keyed by model and benchmark, validate score ranges, and record the table version and retrieval date with each record.
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
def parse(rows, version):
    out = {}
    for model, bench, score in rows:
        if not 0 <= score <= 100:
            raise ValueError("score out of range")
        out[(model, bench)] = {"score": score, "version": version}
    return out
t = parse([("carbon", "index", 59), ("argon", "index", 50)], "v5.0")
assert t[("carbon", "index")]["score"] == 59
```

## Failure Modes
- A score and its model row drift apart during extraction and numbers attach to the wrong model.
- Range validation is skipped and a mis-scaled percentage is stored as a score.
- The table version is dropped and scores from different index versions are compared.
- Ties are parsed as one row and a model silently disappears.
- Missing entries are filled with zeros instead of being reported as gaps.

## Security and Authority Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result, and it never treats parsed content as trusted instructions.

## Evidence
- the Gemini 4 Carbon launch reported first place on version 5.0 of the Artificial Analysis Intelligence Index with 59 points against 50 for Argon (blog.luandnh.com, dated October 29, 2026) ([public signal](https://blog.luandnh.com/en/ai-daily/2026-10-29/))
- These are dated public signals, not adoption metrics; this contract claims no production hardening beyond the recorded evidence.

## Related Skills
- [Complexity Claim Verification Reasoning](../02-reasoning/complexity-claim-verification-reasoning.md)
- [Model Release Ledger Maintenance](../12-data/model-release-ledger-maintenance.md)

## Changelog
| Version | Date | Notes |
|---|---|---|
| `v1` | `2026-10` | Initial evidence-backed contract. |
