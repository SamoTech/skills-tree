---
name: etl-pipeline
description: Design or execute extract-transform-load pipelines with idempotent stages, reconciled counts, and verified checkpoints.
metadata:
  source: skills/12-data/etl-pipeline.md
  category: 12-data
  version: "v2"
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-12-data-etl-pipeline.json)

# Etl Pipeline

**Category:** `data`
**Skill Level:** `advanced`
**Stability:** `stable`
**Added:** 2025-03

### Description

Design or execute extract-transform-load pipelines with idempotent stages, reconciled counts, and verified checkpoints. The data step is contract-first: validate the input contract before transforming, and verify the output against explicit expectations rather than trusting the pipeline.

### Inputs / Outputs

| Direction | Field | Type | Contract |
|---|---|---|---|
| Input | source | object | The upstream system with its change semantics (full/incremental/CDC) |
| Input | pipeline_spec | object | Extraction, transformation, and load contracts with idempotency keys |
| Output | load_result | object | Rows extracted, transformed, loaded, and rejected per stage |
| Output | run_id | string | A deterministic identifier making reruns idempotent |

### Procedure
1. Define the extraction scope (full, incremental, CDC) and its checkpoint before running.
2. Make every load idempotent: rerunning a stage must not duplicate rows.
3. Validate each stage's output count against its input count and rejects.
4. Fail the run on reconciliation mismatch instead of loading partial data.
5. Record the checkpoint only after a stage's outputs are verified.
6. Emit a run report with per-stage counts and the final checkpoint.

### Example

```python
stages = [{'name': 'extract', 'in': 100, 'out': 100}, {'name': 'transform', 'in': 100, 'out': 98, 'rejected': 2}, {'name': 'load', 'in': 98, 'out': 98}]
checkpoint = None
for s in stages:
    expected = s['in'] - s.get('rejected', 0)
    assert s['out'] == expected, 'stage not reconciled: ' + s['name']
    checkpoint = s['name']
assert checkpoint == 'load'
print({'stages_ok': len(stages), 'final_checkpoint': checkpoint})
```

### Related Skills

- [Incremental Processing](incremental-processing.md) - process only new data per run
- [Change Data Capture](change-data-capture.md) - stream source changes instead of polling
- [Data Validation](data-validation.md) - validate stage outputs

## Failure Modes

- Non-idempotent loads duplicating data on every rerun.
- Checkpoints advanced before outputs were verified, losing work on crash.
- Stage counts not reconciled, silently dropping rejected rows.
- No run id, so partial runs cannot be identified or retried safely.

## Changelog
- v2 (2026-11): Structural modernization; added the input/output contract table, a skill-specific execution procedure, a deterministic example, and corpus-verified related links (replaced the unresolvable cross-category related references).
- v1 (2025-03): Initial entry.

## Evidence

- https://agentskills.io/specification

Evidence status: implementation guidance only; runtime behavior must be checked against the executing pipeline's documentation; no benchmark claim is made without reproducible evidence.
