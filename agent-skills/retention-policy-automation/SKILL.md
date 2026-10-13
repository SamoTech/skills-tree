---
name: retention-policy-automation
description: Automate data retention enforcement with policy-as-code rules, deletion manifests, and verifiable audit output for every expired record.
metadata:
  source: skills/12-data/retention-policy-automation.md
  category: 12-data
  version: "v1"
---

# Retention Policy Automation

## Description
Automate data retention enforcement with policy-as-code rules, deletion manifests, and verifiable audit output for every expired record. The procedure is constrained by explicit inputs and acceptance criteria rather than best-effort judgment alone.

## When to Use
- retention rules must be enforced with an auditable record of what was deleted.
- Ambiguity or missing evidence would change the outcome.
- The result must be recorded with reasons and evidence for later verification.

## Inputs / Outputs
| Area | Contract |
|---|---|
| Inputs | Task context, candidate inputs, and explicit acceptance criteria for retention policy automation work. |
| Outputs | A decision or artifact with recorded reasons, rejected alternatives, and verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Define the goal, the constraints, and the boundary of what this procedure may change.
2. Inventory the available inputs and flag gaps or ambiguities that block progress.
3. Execute the retention policy automation steps in a bounded, checkpointed way.
4. Compare the actual outcome against the expected outcome and record deviations.
5. On failure, apply the declared fallback path, and never widen permissions to recover.
6. Emit a structured result with evidence and provenance for downstream consumers.

## Runnable Example
```python
def expired(records, policy_days, now_day):
    out = []
    for record in records:
        if now_day - record['created_day'] > policy_days:
            out.append(record['id'])
    return out

records = [{'id': 'r1', 'created_day': 0}, {'id': 'r2', 'created_day': 90}]
assert expired(records, 30, 100) == ['r1']
```

## Failure Modes
- Deleting without a manifest of exactly what was removed.
- Policies that ignore legal holds still in force.
- Clock-based expiry with no timezone or epoch recorded.
- Deletion jobs that fail silently and leave data in place.
- No dry-run comparison before the first live enforcement.

## Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result.

## Evidence
Policy-as-code retention enforcement appears in 2026 data-governance requests; this is a dated signal, not an adoption metric.

## Related
- data-anonymization.md
- data-contract-enforcement.md
- data-lineage.md
