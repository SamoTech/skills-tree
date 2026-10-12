---
name: data-contract-enforcement
description: Define and enforce machine-readable data contracts covering schema, types, ranges, and freshness, failing production pipelines loudly when producers drift from the agreed shape.
metadata:
  source: skills/12-data/data-contract-enforcement.md
  category: 12-data
  version: "v1"
---

# Data Contract Enforcement

Category: Data | Level: intermediate | Stability: experimental | Version: v1

## Description

A data contract is an executable agreement between a producer and a consumer. The skill covers expressing the contract as code: field names, types, ranges, nullability, and freshness expectations, then enforcing it at handoff boundaries so that a producer change surfaces as a loud, attributable failure in the producer pipeline rather than silent corruption downstream. Failures are reported with the violated clause, not a generic schema error.

## When to Use

Use when a data set crosses a team or system boundary and downstream consumers must be protected from silent schema and quality drift.

Do not enforce contracts only in tests. Without enforcement at the production handoff, producers can ship breaking changes at any time and consumers absorb them silently.

## Inputs

| Input | Type | Required | Description |
|---|---|---|---|
| `contract` | `object` | Yes | Machine-readable schema, types, ranges, and freshness rules |
| `dataset` | `table` | Yes | The batch or stream being validated at the boundary |
| `enforcement` | `enum` | No | `fail` (default) or `quarantine` for low-trust transitions |

## Procedure

1. Express the contract in code: fields, types, ranges, nullability, and freshness windows.
2. Version the contract and record which version each producer declares.
3. Validate the incoming data set at the handoff boundary, collecting every violation.
4. Fail or quarantine the batch on violation; never pass degraded data through as if clean.
5. Report violations by clause with producer, contract version, and offending records.
6. Negotiate contract changes as versioned migrations with consumer sign-off before rollout.

## Outputs

| Output | Type | Description |
|---|---|---|
| `validation_result` | `object` | Pass or fail verdict with the clause-level evidence |
| `violations` | `array` | Each violated rule with sample offending records |
| `contract_version` | `string` | The contract version the data was validated against |

## Runnable Example

```python
def enforce_contract(rows, contract):
    """rows: dicts; contract: {field: (type, min, max)}"""
    violations = []
    for i, row in enumerate(rows):
        for field, (ftype, lo, hi) in contract.items():
            if field not in row:
                violations.append({"row": i, "field": field, "rule": "required"})
                continue
            v = row[field]
            if not isinstance(v, ftype):
                violations.append({"row": i, "field": field, "rule": "type"})
            elif v < lo or v > hi:
                violations.append({"row": i, "field": field, "rule": "range", "value": v})
    return {"verdict": "pass" if not violations else "fail", "violations": violations}

print(enforce_contract(
    [{"qty": 3, "price": 9.5}, {"qty": -1, "price": 4.0}],
    {"qty": (int, 0, 1000), "price": (float, 0.0, 10000.0)},
))
```

## Failure Modes

| Failure Mode | Cause | Mitigation |
|---|---|---|
| Silent schema drift | Contract not enforced at the boundary | Validate at handoff, not only in tests |
| Generic failure reports | Violations collapsed into one schema error | Report per clause with sample records |
| Contract and code diverge | Contract edited without producer sign-off | Version contracts and review migrations |
| Freshness never checked | Only structure enforced | Include freshness windows in the contract |
| Quarantine fills up | Failing batches parked without owners | Alert on quarantine depth and assign triage |

## Security and Authority Boundary

Contracts describe data an organization may be legally accountable for. Keep contract definitions in version control with review, log validation outcomes for audit, and never relax a contract to let a failing producer through without a recorded decision.

## Evidence

This skill is grounded in dated public implementation references:

1. The Pandera library for DataFrame schema validation and enforcement (https://github.com/pandera-dev/pandera).
2. The Great Expectations project for data quality assertions at handoff boundaries (https://greatexpectations.io/).

Honest boundary: these are implementation references, not adoption or demand evidence; this entry was added under the owner-directed corpus expansion recorded in `meta/memory/DECISIONS.md`, and no demand signal is claimed for it.

## Related Skills

- [Data Validation](data-validation.md) — the underlying assertion engine contracts build on.
- [Schema Inference](schema-inference.md) — the discovery step used to draft the first contract from real data.

## Changelog

| Date | Version | Change |
|---|---|---|
| `2026-10` | v1 | Initial entry added under the owner-directed corpus expansion |
