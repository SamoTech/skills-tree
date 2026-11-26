---
name: inductive-reasoning
description: Generalize from observations to tentative broader conclusions while preserving sample limits, counterexamples, and uncertainty.
metadata:
  source: skills/02-reasoning/inductive-reasoning.md
  category: 02-reasoning
  version: "v3"
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-02-reasoning-inductive-reasoning.json)

# Inductive Reasoning

**Category:** `reasoning`
**Skill Level:** `intermediate`
**Stability:** `stable`
**Added:** 2025-03

### Description

Generalize from specific observations to broader principles or likely conclusions, always carrying the sample size, selection basis, counterexamples, and uncertainty alongside the generalization.

### Inputs / Outputs

| Direction | Field | Type | Contract |
|---|---|---|---|
| Input | `observations` | list of records | The specific cases; each must state how it was selected |
| Input | `hypothesis` | string | The tentative generalization to test against the observations |
| Output | `generalization` | string | The bounded conclusion, with its support stated |
| Output | `sample_limits` | list of string | Sample size, selection basis, and coverage gaps |
| Output | `counterexamples` | list of records | Observed cases the generalization does not cover |

### Procedure
1. State the candidate generalization before searching the observations for support.
2. Count the observations and record how they were selected; convenience samples bound the claim.
3. Search actively for counterexamples, including cases outside the observed range.
4. State the generalization as a tentative hypothesis with its sample limits attached.
5. Distinguish extrapolation inside the observed range from extrapolation beyond it.
6. Name the observation that would most weaken the conclusion and how to check for it.

### Example

```python
def support_ratio(observations: list[bool], sample_basis: str) -> dict:
    """Bound an inductive claim by its observed support and selection basis."""
    supporting = sum(observations)
    n = len(observations)
    return {
        "supporting": supporting,
        "total": n,
        "ratio": round(supporting / n, 3) if n else None,
        "claim_strength": "tentative" if n < 30 else "moderate",
        "sample_basis": sample_basis,
    }

print(support_ratio(
    observations=[True, True, False, True, True, True, False, True],
    sample_basis="first 8 requests after the index change, single table",
))
```

### Failure Modes

- **Hasty generalization:** broad rules from few or unrepresentative observations; state the sample size and selection basis with every generalization.
- **Ignoring counterexamples:** a single counterexample bounds a generalization; record counterexamples rather than explaining them away.
- **Trend extrapolation:** extending a pattern beyond its observed range, or treating a coincidental run as a law.
- **Frequency-as-probability:** an inductive conclusion is a tentative hypothesis with stated limits, not a measured probability.
- **Confirmation search:** seeking only supporting cases; the procedure requires an explicit counterexample search.

### Related Skills

- [Deductive Reasoning](deductive-reasoning.md)
- [Statistical Analysis](../12-data/statistical-analysis.md)

## Changelog
- v3 (2026-11): Structural modernization; added the input/output contract table, procedure, and deterministic support-ratio example.
- v1 (2025-03): Initial entry.

## Evidence
The canonical skill file is the authoritative repository implementation. Repository schema, validation workflows, and the Agent Skills projection contract define structural conformance. Implementation guidance must remain traceable to supplied or independently verified authoritative sources; no benchmark claim is made without reproducible evidence.
