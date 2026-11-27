---
title: "Probabilistic Reasoning"
category: 02-reasoning
level: intermediate
stability: stable
version: v3
description: "Reason with probability distributions and conditional uncertainty while making independence assumptions and prior information explicit."
added: "2025-03"
related: [bayesian-reasoning, reasoning-under-uncertainty, uncertainty-quantification]
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-02-reasoning-probabilistic-reasoning.json)

# Probabilistic Reasoning

**Category:** `reasoning`
**Skill Level:** `intermediate`
**Stability:** `stable`
**Added:** 2025-03

### Description

Reason with probability distributions and conditional uncertainty while making independence assumptions and prior information explicit. Every computed probability is conditional on a declared model: state the priors, the likelihoods, and any independence assumptions before trusting the result.

### Inputs / Outputs

| Direction | Field | Type | Contract |
|---|---|---|---|
| Input | model | object | The events, prior probabilities, and likelihoods, with sources stated |
| Input | evidence | object | The observed event(s), precisely defined |
| Output | probabilities | object | Joint, conditional, or marginal results in [0, 1] |
| Output | assumptions | list of string | The independence and prior assumptions the result depends on |

### Procedure
1. Define the events and the evidence precisely; ambiguous event definitions invalidate the math.
2. State the priors and their source; a guessed prior bounds the result's meaning.
3. Declare every independence assumption; correlated evidence treated as independent overconfides.
4. Compute joint, conditional, and marginal probabilities with the declared model.
5. Report the result together with its assumptions, or report the model gap when inputs are missing.

### Example

```python
def prob_a_and_b_independent(p_a, p_b):
    for p in (p_a, p_b):
        if not 0 <= p <= 1:
            raise ValueError("probabilities must be in [0, 1]")
    return p_a * p_b  # valid ONLY under the independence assumption

p_rain, p_sprinkler = 0.3, 0.6
joint_independent = prob_a_and_b_independent(p_rain, p_sprinkler)
assert round(joint_independent, 6) == 0.18
# Correlated case: sprinkler and rain are NOT independent; the product overestimates.
assumptions = ["rain and sprinkler treated as independent (declared, likely false)"]
print({"P(A and B)": joint_independent, "assumptions": assumptions})
```

### Related Skills

- [Bayesian Reasoning](bayesian-reasoning.md) - posterior updates from evidence
- [Reasoning Under Uncertainty](reasoning-under-uncertainty.md) - hedged decisions under incomplete knowledge
- [Uncertainty Quantification](uncertainty-quantification.md) - representing uncertainty explicitly

## Failure Modes

- Independence assumed for correlated events, producing overconfident probabilities.
- Priors ignored or chosen silently, so the result looks more objective than it is.
- Event definitions ambiguous enough that two valid models give different answers.
- Precise-looking outputs reported without the assumptions they depend on.
- Zero-probability evidence under the model left undefined instead of flagged.

## Changelog
- v3 (2026-11): Structural modernization; reconciled the frontmatter version declaration with the changelog, added the input/output contract table, a deterministic dependency-free example, an execution procedure, and corpus-verified related links.
- v1 (2026-04): Initial entry.

## Evidence

- https://agentskills.io/specification

Evidence status: implementation guidance only; no benchmark claim is made without reproducible evidence.
