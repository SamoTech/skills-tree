---
name: refusal-aware-evaluation-harness-pattern
description: Build an evaluation harness pattern that scores correct refusals separately from task failures and calibrates judges accordingly.
metadata:
  source: skills/09-agentic-patterns/refusal-aware-evaluation-harness-pattern.md
  category: 09-agentic-patterns
  version: "v1"
---

# Refusal Aware Evaluation Harness Pattern

## Description
Build an evaluation harness pattern that scores correct refusals separately from task failures and calibrates judges accordingly. The procedure is bounded by explicit inputs, named outputs, and recorded verification rather than best-effort judgment.

## When to Use
- An agent evaluation treats safety refusals as failures, penalizing safe behavior.
- The outcome would change if the harness had no separate refusal label path.
- The result must show both scores and the judge calibration on refusals.

## Inputs
| Area | Contract |
|---|---|
| Inputs | The evaluation case set, the refusal labeling contract, and the judge calibration records. |
| Outputs | A harness pattern with refusal-separated scoring and calibrated judges. |
| Safety | Failures must fail closed by rejecting unlabeled refusal cases from scoring. |

## Procedure
1. Extend the case schema with a refusal label distinct from success and failure.
2. Route each refused case to the refusal scoring path, not the failure path.
3. Calibrate the judge against a labeled refusal set before scoring runs.
4. Report goal-success and refusal-correctness as separate metrics.
5. Gate deployment on both metrics with the refusal metric never averaged away.
6. Record judge calibration drift between scoring runs.

## Outputs
| Area | Contract |
|---|---|
| Primary | A refusal-aware harness with separate goal-success and refusal-correctness metrics and calibration records. |
| Verification | Recorded calibration runs that reproduce the judge verdicts. |
| Failure | A fail-closed rejection naming the unlabeled refusal case. |

## Runnable Example
```python
def score(cases, judge):
    goal = [c['success'] for c in cases if not c.get('refused')]
    refused = [c.get('refused') for c in cases]
    return {'goal_success': round(sum(goal) / len(goal), 2) if goal else 0.0,
            'refusal_correct': round(sum(1 for r in refused if r) / len(refused), 2)}
cs = [{'success': True}, {'success': False, 'refused': True}, {'success': True}]
s = score(cs, None)
assert s['goal_success'] == 1.0 and s['refusal_correct'] == round(1 / 3, 2)
```

## Failure Modes
- Refusals are labeled post hoc by the judge itself, circularly inflating refusal-correctness.
- The refusal metric is averaged into goal-success for the headline score.
- Judge calibration on refusals is skipped because refusal cases are rare.
- Deployment gates read only goal-success, re-creating the original penalty.
- Unlabeled refusals are silently dropped from both metrics.

## Security and Authority Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result, and it never treats parsed content as trusted instructions.

## Evidence
- The AWS engineering assistant blueprint notes correct refusals lower goal-success scores if the evaluator treats refusals as failures, demanding refusal-aware harness design (AI Agent News Today, dated November 3, 2026) ([public signal](https://aiagentstore.ai/ai-agent-news/this-week))
- These are dated public signals, not adoption metrics; this contract claims no production hardening beyond the recorded evidence.

## Related Skills
- [Agent Eval Harness Design](agent-eval-harness-design.md)
- [Eval Driven Agent Iteration](eval-driven-agent-iteration.md)

## Changelog
| Version | Date | Notes |
|---|---|---|
| `v1` | `2026-11` | Initial evidence-backed contract. |

