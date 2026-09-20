---
title: "Bayesian Reasoning"
category: 02-reasoning
level: intermediate
stability: stable
description: "Update a belief from prior probability and evidence likelihoods using Bayes theorem while exposing the assumptions used to compute the posterior."
added: "2025-03"
version: v2
related: [probabilistic-reasoning, reasoning-under-uncertainty, causal]
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-02-reasoning-bayesian-reasoning.json)

# Bayesian Reasoning
Category: reasoning | Level: intermediate | Stability: stable | Version: v2

## Description
Bayesian reasoning updates a prior belief using evidence likelihoods.
The posterior is conditional on the chosen model, prior, likelihood, and evidence definition; it is not a measure of certainty by itself.
The reference implementation is a scalar binary-hypothesis update so the arithmetic is transparent and deterministic.

## Inputs / Outputs
| Input | Type | Contract |
|---|---|---|
| `prior` | `float` | Probability in `[0, 1]` for hypothesis `H` before evidence |
| `p_e_given_h` | `float` | `P(E|H)` in `[0, 1]` |
| `p_e_given_not_h` | `float` | `P(E|not H)` in `[0, 1]` |
| `evidence` | `bool` | Whether `E` is observed; `False` means `not E` |

| Output | Type | Contract |
|---|---|---|
| `posterior` | `float` | `P(H|E)` or `P(H|not E)` in `[0, 1]` |

## Deterministic Reference Implementation
```python
def bayes_update(prior, p_e_given_h, p_e_given_not_h, evidence=True):
    values = (prior, p_e_given_h, p_e_given_not_h)
    if any(not 0 <= value <= 1 for value in values):
        raise ValueError("probabilities must be between 0 and 1")
    if evidence:
        numerator = p_e_given_h * prior
        denominator = numerator + p_e_given_not_h * (1 - prior)
    else:
        numerator = (1 - p_e_given_h) * prior
        denominator = numerator + (1 - p_e_given_not_h) * (1 - prior)
    if denominator == 0:
        raise ValueError("evidence has zero probability under the model")
    return numerator / denominator

posterior = bayes_update(0.30, 0.90, 0.05)
assert round(posterior, 3) == 0.885
```

## Interpretation Protocol
1. Define the hypothesis before looking at the evidence.
2. State the prior source or assumption.
3. Define the evidence event precisely.
4. Specify both likelihoods for a binary model.
5. Compute the posterior without rounding intermediate values.
6. Report sensitivity when the prior or likelihood estimates are uncertain.

## Failure Modes
| Cause | Observable result | Mitigation |
|---|---|---|
| Base-rate neglect | Posterior dominated by a vivid observation | Validate the prior against the target population |
| Dependent evidence treated as independent | Overconfident posterior | Model joint likelihoods or condition sequentially |
| Poor likelihood estimates | Precise-looking but weak result | Report source and uncertainty for likelihoods |
| Zero evidence probability | Undefined update | Revisit the model and evidence definition |
| Selection bias | Prior does not represent observed population | Re-estimate from the relevant sampling frame |

## Validation Rules
- All probabilities must lie in `[0, 1]`.
- The denominator must be positive.
- Posterior must remain in `[0, 1]`.
- Evidence assumptions must be stated before treating multiple observations as independent.
- Numerical output must not be presented as stronger evidence than the underlying model.

## Frameworks
| Framework | Role | Boundary |
|---|---|---|
| Python | Exact scalar arithmetic in the reference example | No uncertainty estimation beyond supplied inputs |
| SciPy | Statistical distributions and tests | Validate model assumptions separately |
| PyMC | Probabilistic models and posterior inference | Sampling diagnostics are required; not a drop-in replacement for scalar Bayes |

## Safety Boundaries
Do not use an unvalidated posterior as a sole basis for medical, legal, financial, employment, or other high-impact decisions.
A Bayesian calculation cannot repair biased evidence, an invalid causal model, or an unrepresentative prior.

## Provenance
The reference example uses elementary Bayes arithmetic and does not claim any external dataset or empirical prior.
Framework compatibility is descriptive; consuming projects must verify their installed versions independently.

## Related
- `probabilistic-reasoning.md` — broader probabilistic inference
- `reasoning-under-uncertainty.md` — uncertainty handling
- `causal.md` — causal assumptions and interventions

## Changelog
- v1 (2026-04): Initial entry
- v2 (2026-09-20): Added explicit Bayesian contract, deterministic implementation, interpretation protocol, validation, failure modes, safety boundaries, and provenance
