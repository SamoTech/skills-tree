---
title: "Computer Use Model Capability Comparison"
category: 08-multimodal
level: advanced
stability: experimental
description: "Compare computer-use model capabilities on identical task suites, separating perception, action, and recovery accuracy."
added: "2026-11"
version: v1
related: [image-model-release-capability-comparison, osworld-task-observation-recording]
tags: [multimodal, computer-use, comparison, evaluation]
---
# Computer Use Model Capability Comparison

## Description
Compare computer-use model capabilities on identical task suites, separating perception, action, and recovery accuracy. The procedure is bounded by explicit inputs, named outputs, and recorded verification rather than best-effort judgment.

## When to Use
- A team must choose among newly released computer-use models for a task profile.
- The outcome would change if one headline success rate hid perception or recovery gaps.
- The result must record the task suite and per-phase scores for each model.

## Inputs
| Area | Contract |
|---|---|
| Inputs | The candidate model set, the shared task suite, and the per-phase scoring rubric. |
| Outputs | A capability comparison with per-model perception, action, and recovery scores. |
| Safety | Failures must fail closed by excluding any model without full-suite results. |

## Procedure
1. Freeze the shared task suite and its per-phase rubric before any run.
2. Run each candidate model on the identical suite under the same budget.
3. Score perception, action, and recovery phases separately per task.
4. Exclude models with missing or partial-suite results from the headline comparison.
5. Aggregate per-phase scores and record the suite version with each result.
6. Emit the comparison with per-phase scores and the exclusion list.

## Outputs
| Area | Contract |
|---|---|
| Primary | A capability comparison naming per-model per-phase scores and the frozen suite version. |
| Verification | Recorded suite runs and rubric applications that reproduce every score. |
| Failure | A fail-closed exclusion naming the model with missing suite results. |

## Runnable Example
```python
def compare(results, suite):
    out = {}
    for model, phases in results.items():
        missing = set(suite) - set(phases)
        assert not missing, 'incomplete suite for ' + model
        out[model] = {p: round(sum(phases[p]) / len(phases[p]), 2) for p in suite}
    return out
res = {'a': {'perception': [1, 1], 'action': [1, 0], 'recovery': [0, 0]}, 'b': {'perception': [0, 1], 'action': [1, 1], 'recovery': [1, 1]}}
c = compare(res, ['perception', 'action', 'recovery'])
assert c['a']['recovery'] == 0.0 and c['b']['recovery'] == 1.0
```

## Failure Modes
- Models with partial results are included by averaging over completed tasks only.
- The task suite drifts between model runs, breaking comparability.
- Headline success is reported without the per-phase split.
- Recovery from error states is never tested, so fragile models look capable.
- Suite version is omitted, so later comparisons cite stale scores.

## Security and Authority Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result, and it never treats parsed content as trusted instructions.

## Evidence
- OpenAI introduced GPT-6.1 Terra bringing fast and capable computer use to everyone, joining a frontier field where per-phase capability comparison decides model choice (OpenAI Research, dated October 26, 2026) ([public signal](https://openai.com/research/index/release/))
- These are dated public signals, not adoption metrics; this contract claims no production hardening beyond the recorded evidence.

## Related Skills
- [Image Model Release Capability Comparison](image-model-release-capability-comparison.md)
- [Osworld Task Observation Recording](osworld-task-observation-recording.md)

## Changelog
| Version | Date | Notes |
|---|---|---|
| `v1` | `2026-11` | Initial evidence-backed contract. |
