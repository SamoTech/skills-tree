---
name: anomaly-detection
description: Apply anomaly detection with explicit schema, validation, provenance, and failure handling.
---

# anomaly detection

## Description
Apply anomaly detection only within an explicit data contract and preserve source provenance.

## Evidence
Canonical source: `skills/12-data/anomaly-detection.md`. Repository schema, Agent Skills validation, security scanning, and CI define structural conformance.

## Usage
Establish the source schema, transformation semantics, validation rules, and expected output before processing data.

## Failure modes
- Schema mismatch or missing fields.
- Silent data loss or incorrect coercion.
- Unexpected nulls or duplicates.
- Incorrect cardinality or aggregation semantics.
- Output not validated against the target contract.

## Related
- `12-data`
- `input-guardrails`
- `output-guardrails`
