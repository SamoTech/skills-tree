---
name: synthetic-data-generation
description: Generate artificial data sets that preserve the statistical structure of a source or a specification, for testing, development, and demonstrations, without exposing real records.
metadata:
  source: skills/12-data/synthetic-data-generation.md
  category: 12-data
  version: "v1"
---

# Synthetic Data Generation

Category: Data | Level: intermediate | Stability: experimental | Version: v1

## Description

Synthetic data replaces sensitive or scarce data with records generated from a model or a specification. The skill covers choosing a generation strategy: fully synthetic from declared distributions, or fitted to a source with constraints that prevent memorization, then validating the output for statistical fidelity, referential integrity, and leakage of real records. The output is labeled synthetic, with its provenance recorded so it can never be mistaken for production data.

## When to Use

Use when development, testing, or demonstrations need realistic data volumes and shapes without access to real personal or proprietary records.

Do not present synthetic data as a privacy solution by default. Naive fitting can memorize rare records; privacy claims require measurement, not generation method labels.

## Inputs

| Input | Type | Required | Description |
|---|---|---|---|
| `specification` | `object` | Yes | Declared distributions and constraints, or a fitted model spec |
| `volume` | `int` | Yes | Number of records to generate |
| `constraints` | `object` | No | Referential, range, and consistency rules the output must satisfy |

## Procedure

1. Declare the schema and per-field distributions, or fit distributions to a source sample.
2. State the fidelity target: which statistics and correlations the output must preserve.
3. Generate records with a fixed seed for reproducibility, applying constraints during generation.
4. Validate the output for schema conformance, statistical fidelity, and referential integrity.
5. Check for leakage: nearest-neighbor overlap with any real source records must be explained.
6. Label the data set synthetic with provenance, seed, and generator version.

## Outputs

| Output | Type | Description |
|---|---|---|
| `synthetic_dataset` | `table` | Generated records satisfying the specification and constraints |
| `fidelity_report` | `object` | Distance between source and synthetic statistics |
| `provenance` | `object` | Seed, generator version, and specification used |

## Runnable Example

```python
def leakage_check(real_rare, synthetic, tol=1e-6):
    """real_rare: [tuple of values]; synthetic: [tuple of values]"""
    hits = []
    rset = set(real_rare)
    for row in synthetic:
        if row in rset:
            hits.append(row)
    return {"exact_matches": len(hits), "examples": hits[:3]}

print(leakage_check(
    [(34, "94107", 95000), (61, "12345", 210000)],
    [(34, "94107", 95000), (45, "60601", 71000)],
))
```

## Failure Modes

| Failure Mode | Cause | Mitigation |
|---|---|---|
| Memorized rare records | Generator overfits outliers from a real source | Constrain fitting and run overlap checks |
| Broken referential integrity | Child keys generated without parents | Generate hierarchies in dependency order |
| Implausible combinations | Independent per-field fitting destroys correlations | Model joint structure or post-filter |
| No reproducibility | Unseeded generation cannot regenerate a bug | Fix and record the seed |
| Synthetic data in production | Generated records mixed into real tables | Label provenance and keep stores separate |

## Security and Authority Boundary

Synthetic data lowers exposure but is not automatically safe: a poorly fitted generator can reproduce real individuals. Measure overlap against source data, never mix synthetic and production stores, and label outputs so downstream consumers cannot mistake them for real records.

## Evidence

This skill is grounded in dated public implementation references:

1. The Synthetic Data Vault project for fitted synthetic tabular data (https://github.com/sdv-dev/SDV).
2. The Faker library for specification-driven synthetic records (https://github.com/joke2k/faker).

Honest boundary: these are implementation references, not adoption or demand evidence; this entry was added under the owner-directed corpus expansion recorded in `meta/memory/DECISIONS.md`, and no demand signal is claimed for it.

## Related Skills

- [Data Anonymization](data-anonymization.md) — the alternative path when the source records themselves must be shared with measured risk.
- [Data Validation](data-validation.md) — the gate that proves generated records meet schema and constraint rules.

## Changelog

| Date | Version | Change |
|---|---|---|
| `2026-10` | v1 | Initial entry added under the owner-directed corpus expansion |
