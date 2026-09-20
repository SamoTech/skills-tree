---
title: "Probabilistic Reasoning"
category: 02-reasoning
level: intermediate
stability: stable
description: "Reason with probability distributions and conditional uncertainty while making independence assumptions and prior information explicit."
added: "2025-03"
version: v3
related: [bayesian-reasoning, reasoning-under-uncertainty, uncertainty-quantification]
prerequisites: [inductive-reasoning, reasoning-under-uncertainty]
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-02-reasoning-probabilistic-reasoning.json)

# Probabilistic Reasoning

**Category:** `02-reasoning`  
**Skill Level:** `intermediate`  
**Stability:** `stable`  
**Added:** `2025-03`  
**Version:** `v3`

## Description

Probabilistic reasoning represents uncertainty with probabilities, conditional probabilities, distributions, and explicit assumptions. It is useful when evidence is incomplete, noisy, or probabilistic rather than deterministically true or false.

The central discipline is to distinguish prior information, observed evidence, conditional assumptions, and posterior conclusions. Probability values should not be presented as objective facts unless the data-generating process and estimation method justify them.

## When to Use

Use this skill when an agent must update beliefs after evidence, compare uncertain hypotheses, calculate conditional or joint probabilities, or communicate uncertainty quantitatively. Use Bayesian reasoning when priors and likelihoods are explicitly modeled; use statistical inference when estimating population quantities from samples.

Do not invent probabilities for events without a defensible model, base rate, or elicitation procedure. If only qualitative evidence is available, state that the result is qualitative rather than fabricating numerical precision.

## Inputs and Outputs

| Item | Contract |
|---|---|
| Hypotheses/events | Mutually exclusive or explicitly overlapping events with defined semantics. |
| Prior probabilities | Non-negative values summing to 1 when a complete hypothesis distribution is supplied. |
| Evidence likelihoods | `P(E|H)` values or another explicitly defined conditional model. |
| Evidence | Observed event(s) used to update or condition the distribution. |
| Assumptions | Independence, conditional independence, stationarity, or other modeling assumptions. |
| Output | Valid probability/distribution plus assumptions, evidence used, and interpretation. |

## Core Identities

For events `A` and `B` with `P(B) > 0`:

```text
P(A | B) = P(A ∩ B) / P(B)
P(A ∩ B) = P(A | B) P(B)
P(A) = Σᵢ P(A | Hᵢ) P(Hᵢ)     for a complete mutually exclusive partition {Hᵢ}
P(Hᵢ | E) = P(E | Hᵢ) P(Hᵢ) / P(E)
```

These identities are mathematical contracts. A numerical answer is only as reliable as the probabilities and assumptions supplied to them.

## Deterministic Reference Implementation

The standard-library implementation below performs Bayes' rule for a finite hypothesis set. It validates the distribution rather than silently normalizing malformed input, which makes failures observable and reproducible.

```python
from collections.abc import Mapping


def bayes_update(
    priors: Mapping[str, float],
    likelihoods: Mapping[str, float],
) -> dict[str, float]:
    if not priors:
        raise ValueError("priors must not be empty")
    if set(priors) != set(likelihoods):
        raise ValueError("priors and likelihoods must have identical hypotheses")
    if any(p < 0 or p > 1 for p in priors.values()):
        raise ValueError("each prior must be in [0, 1]")
    if any(p < 0 or p > 1 for p in likelihoods.values()):
        raise ValueError("each likelihood must be in [0, 1]")

    prior_total = sum(priors.values())
    if abs(prior_total - 1.0) > 1e-12:
        raise ValueError("priors must sum to 1")

    weights = {
        hypothesis: priors[hypothesis] * likelihoods[hypothesis]
        for hypothesis in priors
    }
    evidence = sum(weights.values())
    if evidence <= 0:
        raise ValueError("evidence has zero probability under every hypothesis")

    posterior = {hypothesis: weight / evidence for hypothesis, weight in weights.items()}
    assert abs(sum(posterior.values()) - 1.0) < 1e-12
    return posterior


posterior = bayes_update(
    {"H1": 0.7, "H2": 0.3},
    {"H1": 0.9, "H2": 0.2},
)
print({key: round(value, 6) for key, value in posterior.items()})
```

The example is deterministic for the same inputs and has no network, model, or external-library dependency. The resulting posterior is approximately `H1=0.913043` and `H2=0.086957`.

## Validation Rules

- Hypothesis keys must match between priors and likelihoods.
- Every supplied probability must lie in `[0, 1]`.
- A complete prior distribution must sum to `1` within a documented numerical tolerance.
- The evidence denominator must be positive before division.
- Posterior probabilities must sum to `1` within the documented tolerance.
- Independence or conditional-independence assumptions must be stated when used.
- Never silently normalize invalid priors in the reference implementation.

## Failure Modes

| Failure mode | Consequence | Mitigation |
|---|---|---|
| Invalid prior normalization | Posterior is mathematically inconsistent. | Validate the prior sum before updating. |
| Double-counted evidence | Confidence becomes artificially extreme. | Model dependencies and conditional relationships explicitly. |
| Base-rate neglect | Rare hypotheses are overestimated. | Include defensible priors or report missing base-rate information. |
| Zero evidence likelihood | Hypothesis receives zero posterior mass. | Verify whether the likelihood is genuinely zero or merely unmodeled. |
| False independence assumption | Joint probability is distorted. | Test or justify conditional independence. |
| False numerical precision | Users infer certainty from arbitrary decimals. | Report model uncertainty and appropriate significant figures. |

## Safety Boundaries

Probabilities are not guarantees. Do not present an estimated probability as a certainty, diagnosis, intent classification, or factual claim without explaining the model and evidence. For high-impact decisions, expose uncertainty, sensitivity to priors/likelihoods, and important alternative hypotheses. Do not infer sensitive personal attributes from weak proxy variables merely because a probabilistic model can produce a number.

## Provenance and Reproducibility

Record the hypothesis set, prior source, likelihood source, evidence identifiers, model assumptions, numerical tolerance, and update timestamp. A reproducible result must permit the same inputs and equations to regenerate the same posterior.

## Framework Notes

Libraries such as `pgmpy` can represent Bayesian networks and perform inference, but the reference contract above does not require them. A framework may be substituted only when its model semantics, variable domains, dependency structure, and inference behavior are compatible with the declared contract.

## Related Skills

- [Bayesian Reasoning](bayesian-reasoning.md)
- [Reasoning Under Uncertainty](reasoning-under-uncertainty.md)
- [Uncertainty Quantification](uncertainty-quantification.md)
- [Inductive Reasoning](inductive-reasoning.md)

## Changelog

- v3 (2026-09): Added explicit I/O contract, deterministic standard-library Bayes update, validation rules, failure modes, safety boundaries, provenance, and framework boundaries.
- v2 (2026-09): Normalized metadata and related-skill links.
- v1 (2026-04): Initial entry.
