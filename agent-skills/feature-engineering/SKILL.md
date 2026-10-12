---
name: feature-engineering
description: Design and derive model-ready features from raw tables and text, applying scaling, encoding, and windowed aggregation while preventing target leakage and train-serve skew.
metadata:
  source: skills/12-data/feature-engineering.md
  category: 12-data
  version: "v1"
---

# Feature Engineering

Category: Data | Level: intermediate | Stability: experimental | Version: v1

## Description

Feature engineering is where most modeling failures are manufactured. The skill covers profiling raw fields, fitting transforms such as scaling and encoding on the training scope only, deriving past-only windowed aggregates for time-ordered data, encoding categoricals with a fixed vocabulary and an explicit unknown bucket, and validating the resulting matrix for leakage markers and drift. The fitted transform is persisted so inference reproduces training features exactly.

## When to Use

Use when raw data must be transformed into numeric features for statistical or machine-learned models, including encodings, interactions, and time-window aggregates.

Do not compute features from information unavailable at prediction time. Target-derived aggregates and post-outcome fields leak, and they inflate evaluation scores that collapse in production.

## Inputs

| Input | Type | Required | Description |
|---|---|---|---|
| `raw` | `table` | Yes | Source records in their raw, typed form |
| `spec` | `object` | Yes | Feature definitions with transforms, encodings, and windows |
| `fit_scope` | `enum` | No | `training` (default) or `inference`; controls which statistics are learned |

## Procedure

1. Profile each raw field for type, missingness, cardinality, and range before transforming.
2. Fit transforms such as scaling and encoding on the training scope only, then apply elsewhere.
3. Derive windowed aggregates with strictly past-only windows for time-ordered data.
4. Encode categoricals with a fixed vocabulary; unseen levels map to an explicit unknown bucket.
5. Validate the output matrix for leakage markers, missing values, and feature drift.
6. Persist the fitted transform so inference reproduces the training features exactly.

## Outputs

| Output | Type | Description |
|---|---|---|
| `feature_matrix` | `table` | Model-ready features with stable column order |
| `transform_artifacts` | `object` | Fitted statistics needed to reproduce the features |
| `validation_report` | `object` | Leakage checks, missingness, and drift findings |

## Runnable Example

```python
def fit_scaler(values, scope="training"):
    if scope != "training":
        return {"error": "scaler statistics must be fit on training scope only"}
    mean = sum(values) / len(values)
    var = sum((v - mean) ** 2 for v in values) / len(values)
    return {"mean": round(mean, 4), "std": round(var ** 0.5, 4)}

def apply_scaler(values, stats):
    return [round((v - stats["mean"]) / stats["std"], 4) for v in values]

stats = fit_scaler([1, 2, 3, 4, 5])
print(stats)
print(apply_scaler([3, 5], stats))
```

## Failure Modes

| Failure Mode | Cause | Mitigation |
|---|---|---|
| Target leakage | Feature derived from the label or post-outcome data | Audit every feature for prediction-time availability |
| Train-serve skew | Statistics fit on the full data set | Fit on the training scope only and persist the transform |
| Unknown category crash | New levels appear at inference | Map unseen levels to an explicit unknown bucket |
| Window leakage | Aggregates include the current outcome | Enforce past-only windows with an explicit lag |
| Missing value explosion | Naive handling of absent fields | Encode missingness as an explicit signal |

## Security and Authority Boundary

Feature pipelines can encode protected attributes and leak them through proxies. Document the source of every feature, avoid proxies for protected classes unless justified and reviewed, and keep fitted transform artifacts out of public exports.

## Evidence

This skill is grounded in dated public implementation references:

1. The scikit-learn preprocessing guide (https://scikit-learn.org/stable/modules/preprocessing.html).
2. The scikit-learn feature extraction guide (https://scikit-learn.org/stable/modules/feature_extraction.html).

Honest boundary: these are implementation references, not adoption or demand evidence; this entry was added under the owner-directed corpus expansion recorded in `meta/memory/DECISIONS.md`, and no demand signal is claimed for it.

## Related Skills

- [Data Profiling](data-profiling.md) — the pre-transform audit of types, ranges, and missingness.
- [Data Validation](data-validation.md) — the post-transform gate that catches leakage and drift markers.

## Changelog

| Date | Version | Change |
|---|---|---|
| `2026-10` | v1 | Initial entry added under the owner-directed corpus expansion |
