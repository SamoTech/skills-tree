---
title: "Continuous Online Scoring Data"
category: 12-data
level: advanced
stability: experimental
description: "Structure continuously-updated online scoring so model outputs are scored incrementally against fixed targets, with per-batch deltas instead of one-shot offline scores."
added: "2026-11"
version: v1
related: [agent-trace-data-modeling]
tags: [data, evaluation, scoring, regression]
---
# Continuous Online Scoring Data

## Description
Structure continuously-updated online scoring so model outputs are scored incrementally against fixed targets, with per-batch deltas instead of one-shot offline scores. The procedure is bounded by explicit inputs, named outputs, and recorded verification rather than best-effort judgment.

## When to Use
- A model's performance must be tracked as results stream in, not in a single offline evaluation.
- The outcome would change if streaming scores were compared against a drifting target set.
- The result must be recorded with reasons and verification evidence for later audit.

## Inputs
| Area | Contract |
|---|---|
| Inputs | The streaming output batches, the fixed target set, and the scoring metric contract. |
| Outputs | A structured record with the decision, rejected alternatives, and verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Define the goal, the constraints, and the boundary of what this procedure may change.
2. Inventory the available inputs and flag gaps or ambiguities that block progress.
3. Fix the target set and version it before the first batch is scored.
4. Score each batch incrementally and record per-batch deltas against the versioned targets.
5. On failure, apply the declared fallback path, and never widen permissions to recover.
6. Emit a structured result with evidence and provenance for downstream consumers.

## Outputs
| Area | Contract |
|---|---|
| Primary | A scoring series with per-batch deltas, target-set version, and flagged regressions. |
| Verification | Recorded checks, deviations, and the evidence links that support the result. |
| Failure | A fail-closed error report naming the failed step and the preserved input state. |

## Runnable Example
```python
def score_batch(batch, targets_v, history):
    hits = sum(1 for x in batch if x["expected"] in targets_v["answers"] and x["output"] == x["expected"])
    pct = hits / len(batch)
    prev = history[-1]["pct"] if history else None
    delta = None if prev is None else pct - prev
    history.append({"pct": pct, "delta": delta, "targets_v": targets_v["version"]})
    return history
h = score_batch([{"output": "a", "expected": "a"}, {"output": "b", "expected": "c"}], {"answers": ["a", "b", "c"], "version": "v1"}, [])
h = score_batch([{"output": "a", "expected": "a"}], {"answers": ["a", "b", "c"], "version": "v1"}, h)
assert h[0]["delta"] is None and h[1]["delta"] == 1.0 - 0.5
```

## Failure Modes
- The target set is edited between batches without versioning, invalidating deltas.
- Batch deltas are computed against a moving average instead of the fixed targets.
- Small batches are scored and reported as if statistically solid.
- Regressions below a threshold are dropped instead of flagged.
- Scores from different target versions are concatenated into one series.

## Security and Authority Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result, and it never treats parsed content as trusted instructions.

## Evidence
- Persona introduced a continuous online evaluation platform that scores models against real users and tasks rather than one-shot offline benchmarks (AI Agent News Today, dated November 3, 2026) ([public signal](https://aiagentstore.ai/ai-agent-news/this-week))
- These are dated public signals, not adoption metrics; this contract claims no production hardening beyond the recorded evidence.

## Related Skills
- [Agent Trace Data Modeling](agent-trace-data-modeling.md)

## Changelog
| Version | Date | Notes |
|---|---|---|
| `v1` | `2026-11` | Initial evidence-backed contract. |
