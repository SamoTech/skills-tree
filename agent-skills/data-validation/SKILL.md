---
name: data-validation
description: Check datasets against declared constraints — schema, types, ranges, and cross-field rules — before they enter analysis or models, failing loudly at the boundary.
metadata:
  source: skills/12-data/data-validation.md
  category: 12-data
  version: "v1"
---

# Data Validation

Category: Data | Level: intermediate | Stability: experimental | Version: v1

## Description

Data arrives wrong more often than it arrives late: nulls where keys live, strings where numbers were promised, duplicate rows quietly doubling a metric. This skill moves checking to the boundary: constraints are declared alongside the pipeline, every batch is validated on arrival, and a violation stops the data instead of following it downstream. The essential move is declaring expectations explicitly — an undeclared constraint cannot be checked, and an unchecked constraint eventually becomes a wrong number someone acted on.

## When to Use

Use at every ingestion boundary — files, API feeds, database extracts — and before anything feeds reporting, training, or user-visible output.

Do not validate beyond what consumers depend on; a constraint nobody relies on still costs every batch and fails runs for no operational reason.

## Inputs

| Input | Type | Required | Description |
|---|---|---|---|
| `dataset` | `table` | Yes | The batch or table arriving at the boundary |
| `schema` | `schema` | Yes | Declared types, required fields, and nullability |
| `constraints` | `list` | Yes | Value rules — ranges, enums, uniqueness, cross-field logic |

## Procedure

1. Declare the schema first — column names, types, nullability — and version it beside the pipeline that enforces it.
2. Add value constraints that consumers actually rely on: ranges, enum membership, uniqueness of keys, referential joins.
3. Run validation on arrival, per batch, and collect all violations rather than stopping at the first.
4. Route failures by severity: hard violations quarantine the batch, soft ones are logged with counts and rates.
5. Report violation statistics as data — failure rates by rule over time — so drift is visible before it becomes an outage.
6. Change the schema deliberately: a constraint change ships as a reviewed edit with a migration, not as a hotfix to silence a failing rule.

## Outputs

| Output | Type | Description |
|---|---|---|
| `validated` | `table` | The batch that passed, cleared for downstream use |
| `violations` | `table` | Per-record rule failures with the offending values |
| `report` | `map` | Rule-level pass and failure counts for the batch |

## Runnable Example

```python
import pandas as pd

def validate_orders(orders):
    problems = []
    if orders["order_id"].duplicated().any():
        problems.append("duplicate order_id values present")
    bad_amounts = orders[orders["amount"] < 0]
    if not bad_amounts.empty:
        problems.append(f"negative amounts: {len(bad_amounts)} rows")
    missing_status = orders[orders["status"].isna()]
    if not missing_status.empty:
        problems.append(f"missing status: {len(missing_status)} rows")
    return problems

orders = pd.DataFrame({
    "order_id": [1, 2, 2],
    "amount": [10, -5, 30],
    "status": ["paid", None, "paid"],
})
print(validate_orders(orders))
```

## Failure Modes

| Failure Mode | Cause | Mitigation |
|---|---|---|
| Silent coercion | A wrong-typed column parsed into plausible nonsense | Type-check at the boundary; never rely on parse leniency |
| Null smuggling | Missing keys flow into aggregates as zeros or blanks | Declare nullability; fail on missing required fields |
| Duplicate keys | The same record counted twice in a metric | Uniqueness-check primary keys per batch |
| Rule sprawl | Constraints accumulated that nobody depends on | Retire constraints no consumer relies on |
| Failure fatigue | Frequent red pipelines ignored as background noise | Severity-route; only hard violations block |

## Security and Authority Boundary

Validation reports quote offending values: constraint failures on sensitive columns must surface the shape of the violation without reproducing the raw value in logs, and validation stages should inherit the access scope of the data they check.

## Evidence

This skill is grounded in dated public implementation references:

1. The pandera data validation framework documentation (https://pandera.readthedocs.io/).
2. The pandas library documentation (https://pandas.pydata.org/docs/).

Honest boundary: these are implementation references, not adoption or demand evidence; this entry was added under the owner-directed corpus expansion recorded in `meta/memory/DECISIONS.md`, and no demand signal is claimed for it.

## Related Skills

- [Data Cleaning](data-cleaning.md) — repairing the data validation only quarantines.
- [Schema Inference](schema-inference.md) — discovering the shape validation then enforces.

## Changelog

| Date | Version | Change |
|---|---|---|
| `2026-10` | v1 | Initial entry added under the owner-directed corpus expansion |
