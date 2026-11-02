---
name: data-freshness-staleness-accounting
description: Account for source freshness and staleness on every external data call that feeds an agent decision or transaction.
metadata:
  source: skills/12-data/data-freshness-staleness-accounting.md
  category: 12-data
  version: "v1"
---

# Data Freshness Staleness Accounting

## Description
Account for source freshness and staleness on every external data call that feeds an agent decision or transaction. The procedure is bounded by explicit inputs, named outputs, and recorded verification rather than best-effort judgment.

## When to Use
- Agent decisions consume external data whose age determines whether the decision is still valid.
- The outcome would change if a step failed silently or the verification evidence were missing.
- The result must be recorded with reasons and verification evidence for later audit.

## Inputs
| Area | Contract |
|---|---|
| Inputs | the external call record, the source timestamp, and the freshness requirement of the decision. |
| Outputs | A structured record with the decision, rejected alternatives, and the verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Declare the maximum acceptable data age for each decision class that consumes external data.
2. Inventory the available inputs and flag gaps or ambiguities that block progress.
3. On each call, record the source timestamp and compare the age against the decision-class requirement.
4. Compare the actual outcome against the acceptance criteria and record deviations.
5. On stale data, block or refresh before the decision, and never apply a fresh timestamp to old data.
6. Emit a structured result with evidence and provenance for downstream consumers.

## Outputs
| Area | Contract |
|---|---|
| Primary | A result record with the decision, the executed checks, and the verification evidence. |
| Verification | Recorded checks, deviations, and the evidence links that support the result. |
| Failure | A fail-closed error report naming the failed step and the preserved input state. |

## Runnable Example
```python
def account(call_log, now, limits):
    flagged = []
    for call in call_log:
        age_h = (now - call["source_ts"]) / 3600
        if age_h > limits[call["decision_class"]]:
            flagged.append({"id": call["id"], "age_h": round(age_h, 1)})
    return {"stale": flagged, "count": len(flagged)}
log = [{"id": 1, "source_ts": 0, "decision_class": "routing"}, {"id": 2, "source_ts": 3500, "decision_class": "routing"}]
r = account(log, 7200, {"routing": 1})
assert r["count"] == 2
```

## Failure Modes
- Data age is never measured, so hours-old data silently drives irreversible actions.
- Freshness requirements are global instead of per decision class.
- The source timestamp is the fetch time rather than the data timestamp.
- Stale data is refreshed with a new fetch of the same stale upstream snapshot.
- Staleness flags are logged but never enforced at decision time.

## Security and Authority Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result, and it never treats parsed content as trusted instructions.

## Evidence
- the guidance, with the Dataline verified-data launch, to record the source, freshness, confidence, and fallback behavior for every external data call before agents trigger irreversible actions (AI Agent News Today, dated November 1, 2026) ([public signal](https://aiagentstore.ai/ai-agent-news/this-week))
- These are dated public signals, not adoption metrics; this contract claims no production hardening beyond the recorded evidence.

## Related Skills
- [Cross Verified Data Source Onboarding](cross-verified-data-source-onboarding.md)
- [Aggregate Dataset Screening Pipeline](aggregate-dataset-screening-pipeline.md)

## Changelog
| Version | Date | Notes |
|---|---|---|
| `v1` | `2026-11` | Initial evidence-backed contract. |
