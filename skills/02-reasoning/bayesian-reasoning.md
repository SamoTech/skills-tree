![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-02-reasoning-bayesian-reasoning.json)

# Bayesian Reasoning
Category: reasoning | Level: advanced | Stability: stable | Version: v1

## Description
Update beliefs based on evidence using Bayes' theorem: compute posterior probability from prior and likelihood.

## Example
```python
def bayes_update(prior, likelihood_given_true, likelihood_given_false, evidence=True):
    if evidence:
        posterior = (likelihood_given_true * prior) / ((likelihood_given_true * prior) + (likelihood_given_false * (1 - prior)))
    else:
        posterior = ((1 - likelihood_given_true) * prior) / (((1 - likelihood_given_true) * prior) + ((1 - likelihood_given_false) * (1 - prior)))
    return posterior

# Prior 30% chance of spam, 90% of spam has word 'win', 5% of legit has 'win'
print(bayes_update(0.3, 0.9, 0.05))  # 0.885
```

## Frameworks
| Framework | Method |
|---|---|
| Python | `scipy.stats`, `pymc` |
| LangChain | Custom reasoning chain |

## Failure Modes
- Base rate neglect when setting priors
- Independence assumptions violated in real data

## Related
- `probabilistic-reasoning.md` · `causal.md`

## Changelog
- v1 (2026-04): Initial entry
