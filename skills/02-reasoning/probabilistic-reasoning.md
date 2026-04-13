![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-02-reasoning-probabilistic-reasoning.json)

# Probabilistic Reasoning
Category: reasoning | Level: advanced | Stability: stable | Version: v1

## Description
Reason with probabilities: compute joint, conditional, and marginal distributions; handle uncertainty explicitly.

## Example
```python
from pgmpy.models import BayesianNetwork
from pgmpy.factors.discrete import TabularCPD
from pgmpy.inference import VariableElimination
model = BayesianNetwork([("Rain", "Wet"), ("Sprinkler", "Wet")])
cpd_rain = TabularCPD("Rain", 2, [[0.7], [0.3]])
cpd_sprinkler = TabularCPD("Sprinkler", 2, [[0.6], [0.4]])
cpd_wet = TabularCPD("Wet", 2, [[0.9, 0.3, 0.2, 0.05], [0.1, 0.7, 0.8, 0.95]], evidence=["Rain", "Sprinkler"], evidence_card=[2, 2])
model.add_cpds(cpd_rain, cpd_sprinkler, cpd_wet)
infer = VariableElimination(model)
print(infer.query(["Rain"], evidence={"Wet": 1}))
```

## Failure Modes
- Assuming independence when variables are correlated
- Ignoring prior distributions

## Related
- `bayesian-reasoning.md` · `uncertainty-quantification.md`

## Changelog
- v1 (2026-04): Initial entry
