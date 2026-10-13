---
name: inductive-reasoning
description: Generalize from observations to tentative broader conclusions while preserving sample limits, counterexamples, and uncertainty.
metadata:
  source: skills/02-reasoning/inductive-reasoning.md
  category: 02-reasoning
  version: "v2"
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-02-reasoning-inductive-reasoning.json)

# Inductive Reasoning

**Category:** `reasoning`
**Skill Level:** `intermediate`
**Stability:** `stable`
**Added:** 2025-03

### Description

Generalize from specific observations to broader principles or likely conclusions.

### Example

```
Observations:
  - Request A: 2s when table had 1,000 rows
  - Request B: 4s when table had 2,000 rows
  - Request C: 8s when table had 4,000 rows
Generalization: Query time grows exponentially with row count — index needed.
```

## Failure Modes

- **Hasty generalization:** broad rules from few or unrepresentative observations; state the sample size and selection basis with every generalization.
- **Ignoring counterexamples:** a single counterexample bounds a generalization; record counterexamples rather than explaining them away.
- **Trend extrapolation:** extending a pattern beyond its observed range, or treating a coincidental run as a law.
- **Frequency-as-probability:** an inductive conclusion is a tentative hypothesis with stated limits, not a measured probability.

### Related Skills

- [Deductive Reasoning](deductive-reasoning.md)
- [Statistical Analysis](../12-data/statistical-analysis.md)

## Evidence
The canonical skill file is the authoritative repository implementation. Repository schema, validation workflows, and the Agent Skills projection contract define structural conformance. Implementation guidance must remain traceable to supplied or independently verified authoritative sources; no benchmark claim is made without reproducible evidence.
