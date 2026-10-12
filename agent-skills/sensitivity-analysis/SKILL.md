---
name: sensitivity-analysis
description: Measure how much each input drives a model or decision output, varying inputs over stated ranges and ranking their influence before trusting the result.
metadata:
  source: skills/02-reasoning/sensitivity-analysis.md
  category: 02-reasoning
  version: "v1"
---

# Sensitivity Analysis

Category: Reasoning | Level: intermediate | Stability: experimental | Version: v1

## Description

Any computed recommendation rests on inputs with different leverage. Sensitivity analysis varies each input across a stated range, observes the output response, and ranks which inputs actually drive the conclusion — turning a raw model output into a statement of the form: the conclusion holds unless a named assumption moves by more than a stated amount.

## When to Use

Use before committing to a decision, forecast, or model-based recommendation when inputs are uncertain and someone needs to know which uncertainty matters.

Do not report a single-number output without its dominant sensitivities; a point estimate with unranked assumptions is not a decision aid.

## Inputs

| Input | Type | Required | Description |
|---|---|---|---|
| `model` | `callable` | Yes | Function or process mapping inputs to output |
| `ranges` | `map` | Yes | Tested low and high bounds per input |
| `samples` | `int` | No | Monte Carlo draws when joint effects are tested |

## Procedure

1. Freeze the output metric before varying anything; sensitivity to an undefined metric is meaningless.
2. Vary one input at a time across its stated range with others held at nominal values, recording the output response.
3. Rank inputs by output swing and identify which ones cross decision thresholds.
4. Where inputs interact, sample combinations with a Monte Carlo design and report joint effects, not just single-input swings.
5. Report the ranges tested; a sensitivity claim outside the tested range is an extrapolation.
6. State the consequence: which input, moved how far, reverses the conclusion.

## Outputs

| Output | Type | Description |
|---|---|---|
| `ranking` | `list` | Inputs ranked by influence on the output |
| `thresholds` | `map` | Input values at which the decision flips |
| `report` | `map` | Tested ranges, design, and sampled effects |

## Runnable Example

```python
def one_at_a_time(model, nominal, ranges, steps=3):
    base = model(nominal)
    swings = {}
    for key, (low, high) in ranges.items():
        outputs = []
        for frac in (0, 0.5, 1):
            point = dict(nominal)
            point[key] = low + (high - low) * frac
            outputs.append(model(point))
        swings[key] = max(outputs) - min(outputs)
    return {"base": base, "swings": dict(sorted(swings.items(), key=lambda kv: -kv[1]))}

def model(s):
    return s["price"] * (100 - 2 * s["competitor_price"])

print(one_at_a_time(model, {"price": 10, "competitor_price": 20}, {"price": (8, 12), "competitor_price": (15, 25)}))
```

## Failure Modes

| Failure Mode | Cause | Mitigation |
|---|---|---|
| Unranked assumptions | All inputs presented as equally uncertain | Rank by measured output swing |
| Hidden interactions | Single-input swings miss joint effects | Sample combinations where inputs interact |
| Range omission | Sensitivity claimed outside tested ranges | Always report the tested bounds |
| Nominal anchoring | Results conditional on one nominal point | Test alternative nominal values for stability |
| Threshold silence | Nobody knows which change flips the decision | Report decision thresholds explicitly |

## Security and Authority Boundary

Sensitivity analysis can expose which parameters a system is most vulnerable to — including security-relevant ones. Treat high-leverage parameter lists as sensitive when the underlying model is, and do not publish attack-surface rankings for systems that are not yours.

## Evidence

This skill is grounded in dated public implementation references:

1. The SALib sensitivity analysis library documentation (https://salib.readthedocs.io/).
2. Wikipedia's overview of sensitivity analysis (https://en.wikipedia.org/wiki/Sensitivity_analysis).

Honest boundary: these are implementation references, not adoption or demand evidence; this entry was added under the owner-directed corpus expansion recorded in `meta/memory/DECISIONS.md`, and no demand signal is claimed for it.

## Related Skills

- [Uncertainty Quantification](uncertainty-quantification.md) — the representation layer that gives inputs stated ranges.
- [Risk Assessment](risk-assessment.md) — the decision layer that consumes ranked sensitivities.

## Changelog

| Date | Version | Change |
|---|---|---|
| `2026-10` | v1 | Initial entry added under the owner-directed corpus expansion |
