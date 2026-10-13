---
title: "LLM Judge Calibration"
category: 09-agentic-patterns
level: advanced
stability: experimental
description: "Calibrate a model used as an evaluator against a labeled reference set, measure agreement and bias, and gate its verdicts on measured reliability."
added: "2026-10"
version: v1
related: [critic-agent, skill-quality-evaluation, agent-eval-harness-design]
tags: [evaluation, judges, calibration]
---

# LLM Judge Calibration

## Description
Calibrate a model used as an evaluator against a labeled reference set, measure agreement and bias, and gate its verdicts on measured reliability. The procedure is constrained by explicit inputs and acceptance criteria rather than best-effort judgment alone.

## When to Use
- a model is used to grade outputs and its verdicts influence promotion or rejection decisions.
- Ambiguity or missing evidence would change the outcome.
- The result must be recorded with reasons and evidence for later verification.

## Inputs / Outputs
| Area | Contract |
|---|---|
| Inputs | Task context, candidate inputs, and explicit acceptance criteria for llm judge calibration work. |
| Outputs | A decision or artifact with recorded reasons, rejected alternatives, and verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Define the goal, the constraints, and the boundary of what this procedure may change.
2. Inventory the available inputs and flag gaps or ambiguities that block progress.
3. Execute the llm judge calibration steps in a bounded, checkpointed way.
4. Compare the actual outcome against the expected outcome and record deviations.
5. On failure, apply the declared fallback path, and never widen permissions to recover.
6. Emit a structured result with evidence and provenance for downstream consumers.

## Runnable Example
```python
def agreement(judge, reference):
    if len(judge) != len(reference):
        raise ValueError('label sets differ in length')
    return sum(a == b for a, b in zip(judge, reference)) / len(reference)

rate = agreement(['pass', 'fail', 'pass'], ['pass', 'pass', 'pass'])
assert rate < 0.9
print(rate)
```

## Failure Modes
- Trusting a judge score without measuring agreement with a labeled set.
- Reusing a judge across domains without re-calibration.
- Hiding the judge prompt version with each verdict.
- Ignoring position or verbosity bias in the judge.
- Promoting an uncalibrated judge to a blocking gate.

## Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result.

## Evidence
2026 evaluation practice for judge models stresses calibration sets and measured agreement; this is a dated signal, not an adoption metric.

## Related
- critic-agent.md
- skill-quality-evaluation.md
- agent-eval-harness-design.md
