---
title: "Inductive Reasoning"
category: 02-reasoning
level: intermediate
stability: stable
description: "Generalize from observations to tentative broader conclusions while preserving sample limits, counterexamples, and uncertainty."
added: "2025-03"
version: v3
related: [deductive-reasoning, probabilistic-reasoning, statistical-analysis]
prerequisites: [reasoning-under-uncertainty]
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-02-reasoning-inductive-reasoning.json)

# Inductive Reasoning

**Category:** `02-reasoning`  
**Skill Level:** `intermediate`  
**Stability:** `stable`  
**Added:** `2025-03`  
**Version:** `v3`

## Description

Inductive reasoning moves from observed cases to a broader hypothesis that is stronger than any single observation but remains defeasible. A sound induction separates the observations from the generalization, records the sampling frame, and identifies evidence that would weaken or falsify the conclusion.

Induction does not prove a universal claim merely because every observed case agrees with it. The strength of the conclusion depends on coverage, independence, measurement quality, base rates, selection effects, and the presence of plausible counterexamples.

## When to Use

Use this skill when an agent must infer a recurring pattern from examples, logs, experiments, user reports, or historical cases. Prefer explicit inductive reasoning when the available evidence is incomplete and the output should remain a hypothesis rather than a deduction.

Do not use induction to manufacture certainty from a biased sample. If the question requires a quantified probability, use probabilistic or statistical methods in addition to the qualitative induction.

## Inputs and Outputs

| Item | Contract |
|---|---|
| Observations | A finite set of cases with observable attributes and outcomes. |
| Sampling frame | The population or process from which observations were collected, when known. |
| Candidate hypothesis | A proposed pattern/generalization to test against the observations. Optional on input; required as an explicit output. |
| Counterevidence | Known exceptions, contradictory observations, or plausible alternative explanations. |
| Output | Hypothesis, supporting observations, limitations, counterexamples, and confidence rationale. |

## Contract

Given observations `O`, produce a hypothesis `H` such that:

1. Every claimed supporting observation is traceable to an item in `O`.
2. The hypothesis does not claim more scope than the sampling frame supports.
3. Exceptions are retained rather than silently discarded.
4. Correlation is not described as causation without independent causal evidence.
5. Confidence is qualitative unless a justified statistical model is available.
6. The conclusion remains revisable when new observations contradict `H`.

A useful output shape is:

```text
Hypothesis: <generalization>
Observed support: <case identifiers>
Scope: <population/process actually sampled>
Exceptions: <known counterexamples or none observed>
Alternative explanations: <credible alternatives>
Confidence rationale: <why the evidence is weak/moderate/strong>
Next test: <observation that would discriminate between hypotheses>
```

## Deterministic Reference Implementation

The following standard-library example computes a simple proportion from a supplied sample. It intentionally does not infer a universal law; it reports the observed rate and the sampling limitations so an agent can form a bounded hypothesis.

```python
from collections.abc import Iterable


def inductive_summary(observations: Iterable[bool]) -> dict[str, object]:
    values = list(observations)
    if not values:
        raise ValueError("observations must contain at least one case")
    if any(type(value) is not bool for value in values):
        raise TypeError("observations must contain only bool outcomes")

    successes = sum(values)
    total = len(values)
    rate = successes / total
    return {
        "hypothesis": f"The observed success rate is approximately {rate:.3f} in this sample.",
        "sample_size": total,
        "successes": successes,
        "observed_rate": rate,
        "scope": "observed sample only",
        "confidence_rationale": "No population inference is made without a sampling model.",
    }


result = inductive_summary([True, True, False, True, False])
assert result["sample_size"] == 5
assert result["successes"] == 3
assert result["observed_rate"] == 0.6
print(result)
```

Expected output contains `sample_size=5`, `successes=3`, and `observed_rate=0.6`. The implementation is deterministic for the same ordered boolean input and performs no network or model calls.

## Validation Rules

- Reject an empty observation set.
- Reject non-boolean observations in the reference implementation.
- Preserve the exact sample size and numerator used to support the hypothesis.
- State the observed scope explicitly when no population model is supplied.
- Do not convert an observed frequency into a causal claim.
- Require counterexample handling before describing a pattern as robust.

## Failure Modes

| Failure mode | Consequence | Mitigation |
|---|---|---|
| Small sample | Generalization is unstable. | Report sample size and limit scope. |
| Selection bias | Sample may not represent the target population. | Describe sampling frame and collection method. |
| Confirmation bias | Supporting cases are over-weighted. | Search actively for disconfirming cases. |
| Simpson's paradox | Aggregate trend reverses within subgroups. | Stratify important confounders before generalizing. |
| Correlation mistaken for causation | Invalid causal explanation. | Treat causality as a separate claim requiring causal evidence. |
| Concept drift | Historical pattern no longer holds. | Re-test against recent observations. |

## Safety Boundaries

Do not use an inductive pattern as the sole basis for high-impact decisions when the sample is sparse, unrepresentative, or sensitive to subgroup effects. Do not infer protected characteristics, intent, or causality from weak behavioral correlations. When evidence is ambiguous, expose the ambiguity instead of converting it into a definitive claim.

## Provenance and Reproducibility

Record the observation identifiers, collection interval, sampling frame, transformations, exclusions, and hypothesis version. A reproducible inductive result must allow another evaluator to reconstruct which observations supported and contradicted the generalization.

## Related Skills

- [Deductive Reasoning](deductive-reasoning.md)
- [Probabilistic Reasoning](probabilistic-reasoning.md)
- [Statistical Analysis](../12-data/statistical-analysis.md)
- [Reasoning Under Uncertainty](reasoning-under-uncertainty.md)

## Changelog

- v3 (2026-09): Added explicit I/O contract, deterministic reference implementation, validation rules, failure modes, safety boundaries, provenance, and counterexample handling.
- v2 (2026-09): Normalized metadata and related-skill links.
- v1 (2026-04): Initial entry.
