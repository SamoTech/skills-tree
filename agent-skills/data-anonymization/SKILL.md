---
name: data-anonymization
description: Transform data sets to reduce re-identification risk using suppression, generalization, and pseudonymization, with k-anonymity checks and honest reporting of residual risk.
metadata:
  source: skills/12-data/data-anonymization.md
  category: 12-data
  version: "v1"
---

# Data Anonymization

Category: Data | Level: intermediate | Stability: experimental | Version: v1

## Description

Anonymization is measured, not declared. The skill covers classifying fields into direct identifiers, quasi-identifiers, and sensitive attributes, applying the policy of transforms, then measuring what remains: equivalence-class sizes over quasi-identifier combinations, records below threshold, and utility lost to generalization. Output that cannot meet the threshold is suppressed or further generalized rather than passed through with a false label.

## When to Use

Use when data containing personal or identifying elements must be shared, published, or analyzed outside its origin context.

Do not treat column deletion as anonymization. Remaining quasi-identifiers such as postcode, timestamps, and rare value combinations re-identify most individuals when combined.

## Inputs

| Input | Type | Required | Description |
|---|---|---|---|
| `dataset` | `table` | Yes | Records containing direct or quasi-identifying fields |
| `policy` | `object` | Yes | Field-level transforms and the risk threshold the output must meet |
| `checks` | `list` | No | Re-identification checks to run; defaults to k-anonymity over quasi-identifiers |

## Procedure

1. Classify every field as direct identifier, quasi-identifier, sensitive, or neutral before transforming.
2. Apply the policy: suppress or tokenize direct identifiers and generalize quasi-identifiers.
3. Measure residual risk, including k-anonymity over every quasi-identifier combination.
4. Report the equivalence-class distribution and the records that fall below the threshold.
5. Suppress or further generalize below-threshold records instead of passing them through.
6. Document the transforms applied so the output can never be presented as raw source data.

## Outputs

| Output | Type | Description |
|---|---|---|
| `anonymized_dataset` | `table` | Transformed records meeting the stated threshold |
| `risk_report` | `object` | Equivalence-class distribution and residual risk figures |
| `transform_log` | `list` | Per-field transforms applied, for reproducibility and auditing |

## Runnable Example

```python
def k_anonymity(records, quasi, threshold=2):
    """records: dicts; quasi: quasi-identifier field names"""
    groups = {}
    for r in records:
        key = tuple(r[f] for f in quasi)
        groups.setdefault(key, 0)
        groups[key] += 1
    sizes = sorted(groups.values())
    return {
        "k": sizes[0],
        "violating_groups": sum(1 for v in groups.values() if v < threshold),
    }

print(k_anonymity(
    [{"zip": "12345", "age": "30-39"},
     {"zip": "12345", "age": "30-39"},
     {"zip": "94107", "age": "20-29"}],
    ["zip", "age"],
))
```

## Failure Modes

| Failure Mode | Cause | Mitigation |
|---|---|---|
| Re-identification through combination | Quasi-identifiers generalized too coarsely | Measure k over combinations, not per field |
| Over-generalization | Utility destroyed to satisfy the threshold | Tune per-field granularity and report the loss |
| Pseudonyms reversed | Mapping table shipped with the output | Keep the mapping separate and access-controlled |
| Linkage across releases | Same generalization used in two published sets | Vary bins across releases or use privacy-preserving models |
| Free-text leakage | Names remain inside narrative fields | Scan and redact unstructured text, not just columns |

## Security and Authority Boundary

Anonymization failures cause irreversible privacy harm. Never claim the output is anonymous without measuring residual risk, keep re-identification mappings under separate access control, and stop and escalate when the threshold cannot be met instead of shipping weakly protected data.

## Evidence

This skill is grounded in dated public implementation references:

1. The HHS guidance on HIPAA de-identification methods (https://www.hhs.gov/hipaa/for-professionals/special-topics/de-identification/index.html).
2. The NIST Privacy Framework (https://www.nist.gov/privacy-framework).

Honest boundary: these are implementation references, not adoption or demand evidence; this entry was added under the owner-directed corpus expansion recorded in `meta/memory/DECISIONS.md`, and no demand signal is claimed for it.

## Related Skills

- [Data Validation](data-validation.md) — the schema-level gate that runs before transforms to guarantee field types.
- [Data Lineage](data-lineage.md) — the record of which transforms produced the published output.

## Changelog

| Date | Version | Change |
|---|---|---|
| `2026-10` | v1 | Initial entry added under the owner-directed corpus expansion |
