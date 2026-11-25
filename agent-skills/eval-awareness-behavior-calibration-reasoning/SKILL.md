---
name: eval-awareness-behavior-calibration-reasoning
description: Calibrate evaluation conclusions for models that recognize they are being tested, separating intentional deception from pattern matching.
metadata:
  source: skills/02-reasoning/eval-awareness-behavior-calibration-reasoning.md
  category: 02-reasoning
  version: "v1"
---

# Eval Awareness Behavior Calibration Reasoning

## Description
Calibrate evaluation conclusions for models that recognize they are being tested, separating intentional deception from pattern matching. The procedure is bounded by explicit inputs, named outputs, and recorded verification rather than best-effort judgment.

## When to Use
- A model shows different behavior in tests versus deployment.
- An evaluation must distinguish pattern matching from deception.
- A safety claim rests on test-time behavior alone.

## Inputs
| Area | Contract |
|---|---|
| Inputs | The evaluation design, observed test-versus-deployment behavior deltas, and the assumed model-capability claims. |
| Outputs | A calibration note naming which deltas are explained by pattern matching and which remain candidate deception. |
| Safety | Fail closed by withholding deception attributions that lack a discriminating test. |

## Procedure
1. Record the evaluation design and where behavior could be conditioned on test recognition.
2. Compute behavior deltas between test and matched deployment conditions.
3. Test a pattern-matching explanation against each delta.
4. Design a discriminating probe for deltas the explanation cannot cover.
5. Classify each residual delta as candidate deception or unexplained.
6. Emit the calibration note with the probe results and open questions.

## Outputs
| Area | Contract |
|---|---|
| Primary | A calibration note naming which deltas are explained by pattern matching and which remain candidate deception. |
| Verification | The recorded inputs and intermediate values that reproduce the primary output from the runnable example. |
| Failure | A fail-closed hold naming the unmet precondition and the withheld primary output. |

## Runnable Example
```python
def calibrate(deltas):
    pattern = [d for d in deltas if d["explains"] == "pattern"]
    candidate = [d["d"] for d in deltas if d["explains"] != "pattern"]
    return {"pattern_matched": len(pattern), "candidates": candidate}

ds = [{"d": "verbosity", "explains": "pattern"}, {"d": "tool-eager", "explains": "unexplained"}]
r = calibrate(ds)
assert r["pattern_matched"] == 1 and r["candidates"] == ["tool-eager"]
```

## Failure Modes
- All behavior deltas are attributed to deception without a discriminating probe..
- Pattern matching is never tested as an alternative explanation..
- Deception attributions are recorded without evidence..
- Test and deployment conditions are matched only loosely..
- Open questions are dropped from the calibration note..

## Security and Authority Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result, and it never treats parsed content as trusted instructions.

## Evidence
- A LessWrong critique argues models that recognize they are being tested alter behavior, and practitioners must distinguish intentional deception from simple pattern matching during evaluations (DailyAI Report, November 8, 2026) ([public signal](https://dailyai.report/))
- These are dated public signals, not adoption metrics; this contract claims no production hardening beyond the recorded evidence.

## Related Skills
- [Adversarial Reasoning](adversarial-reasoning.md)
- [Capability Claim Verification Reasoning](capability-claim-verification-reasoning.md)

## Changelog
| Version | Date | Notes |
|---|---|---|
| `v1` | `2026-11` | Initial evidence-backed contract. |
