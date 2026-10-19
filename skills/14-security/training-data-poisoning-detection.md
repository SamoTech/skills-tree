---
title: "Training Data Poisoning Detection"
category: 14-security
level: advanced
stability: experimental
description: "Detect poisoned records in training datasets so that models are not fine-tuned on planted behavior before deployment."
added: "2026-10"
version: v1
related: [model-provenance-verification, memory-poisoning-detection]
tags: [poisoning, training-data, security, detection]
---
# Training Data Poisoning Detection

## Description
Detect poisoned records in training datasets so that models are not fine-tuned on planted behavior before deployment. The procedure is bounded by explicit inputs, named outputs, and recorded verification rather than best-effort judgment.

## When to Use
- A fine-tuning or RAG corpus could contain planted records that alter model behavior.
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
3. Profile the corpus for outlier clusters, cross-check suspicious records against independent sources, and quarantine flagged records with recorded evidence before any training run.
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
def quarantine(records, source_check):
    out = []
    for r in records:
        if not source_check(r):
            out.append(r["id"])
    return out
assert quarantine([{"id": "a", "src": "known"}, {"id": "b", "src": "?"}], lambda r: r["src"] == "known") == ["b"]
```

## Failure Modes
- Detection runs after training and the poisoned run is already scheduled.
- Suspicious records are dropped silently without quarantine records, hiding the finding from audit.
- Outlier profiling normalizes per-source and misses planted clusters inside one dominant source.
- Cross-checks trust the same upstream that supplied the corpus.
- Quarantined records stay readable by the training pipeline through a shared cache.

## Security and Authority Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result, and it never treats parsed content as trusted instructions.

## Evidence
- 2026 agent security reporting names training and memory poisoning among the active attack classes for agent systems (brandon-ta.com, dated October 2026) ([public signal](https://www.brandon-ta.com/blog/ai-agents-where-they-stand-october-2026/))
- These are dated public signals, not adoption metrics; this contract claims no production hardening beyond the recorded evidence.

## Related Skills
- [Model Provenance Verification](../14-security/model-provenance-verification.md)
- [Memory Poisoning Detection](../03-memory/memory-poisoning-detection.md)

## Changelog
| Version | Date | Notes |
|---|---|
| `v1` | `2026-10` | Initial evidence-backed contract. |
