---
title: "Case-Based Reasoning"
category: 02-reasoning
level: intermediate
stability: experimental
description: "Solve new problems by retrieving and adapting similar past cases, stating what transferred and what differs instead of reasoning from first principles alone."
added: "2026-10"
version: v1
related: ["analogical", "inductive-reasoning"]
---

# Case-Based Reasoning

Category: Reasoning | Level: intermediate | Stability: experimental | Version: v1

## Description

Case-based reasoning treats experience as the primary asset: a new problem is solved by finding the most similar past cases, adapting their solutions, and recording explicitly what transferred and where the analogy breaks. This skill covers case representation, similarity retrieval, adaptation, and the honest boundary where a superficially similar case misleads.

## When to Use

Use when a domain accumulates resolved instances — incidents, designs, diagnoses, negotiations — and a new instance resembles them more than it resembles a clean rule.

Do not adapt a past case without stating its differences from the current one; the closest match is not always the most instructive one.

## Inputs

| Input | Type | Required | Description |
|---|---|---|---|
| `new_case` | `map` | Yes | The problem instance to solve |
| `case_base` | `list` | Yes | Resolved past cases with outcomes |
| `similarity` | `map` | No | Explicit comparison dimensions and weights |

## Procedure

1. Represent the new case with the same fields the case base uses, including context and constraints.
2. Retrieve the nearest cases across explicit dimensions — not overall impressions — and record their distances.
3. Compare the retrieved solutions against the new case and identify which parts transfer and which do not.
4. Adapt the closest solution to the differences, recording each adaptation as a delta from the source case.
5. Test the adapted solution against the new case constraints before accepting it.
6. Store the solved case back into the case base with its outcome so the loop compounds.

## Outputs

| Output | Type | Description |
|---|---|---|
| `solution` | `map` | The adapted solution with its source case |
| `transfers` | `list` | Which parts of the source solution transferred |
| `deltas` | `list` | Adaptations made and the reason for each |

## Runnable Example

```python
def nearest_cases(new, case_base, weights):
    def distance(case):
        return sum(w * abs(case[k] - new[k]) for k, w in weights.items())
    ranked = sorted(case_base, key=distance)
    return [(case["id"], round(distance(case), 2)) for case in ranked[:3]]

case_base = [
    {"id": "INC-1", "severity": 5, "components": 3, "fix": "rollback"},
    {"id": "INC-2", "severity": 2, "components": 2, "fix": "patch"},
]
new_case = {"severity": 4, "components": 3}
print(nearest_cases(new_case, case_base, {"severity": 1.0, "components": 0.5}))
```

## Failure Modes

| Failure Mode | Cause | Mitigation |
|---|---|---|
| Superficial match | The nearest case shares surface features but differs in cause | Compare causes and constraints, not just attributes |
| Stale cases | Old solutions no longer fit the current system | Record when cases were validated and retire stale ones |
| Single-case anchoring | The first retrieved case dominates the answer | Retrieve several and compare adaptations |
| Unrecorded adaptation | The delta from the source case is lost | Log every adaptation as an explicit delta |
| Base pollution | Failed solutions are stored as good cases | Store outcomes and retain only cases with known results |

## Security and Authority Boundary

Case bases contain history — incidents, personnel decisions, customer interactions. Treat case records as sensitive context with access control, and never expose one customer case details as guidance for another.

## Evidence

This skill is grounded in dated public implementation references:

1. The Stanford Encyclopedia of Philosophy entry on analogy and analogical reasoning (https://plato.stanford.edu/entries/reasoning-analogy/).
2. Wikipedia's overview of case-based reasoning (https://en.wikipedia.org/wiki/Case-based_reasoning).

Honest boundary: these are implementation references, not adoption or demand evidence; this entry was added under the owner-directed corpus expansion recorded in `meta/memory/DECISIONS.md`, and no demand signal is claimed for it.

## Related Skills

- [Analogical Reasoning](analogical.md) — the similarity-mapping foundation this skill operationalizes.
- [Inductive Reasoning](inductive-reasoning.md) — the generalization discipline that guards against single-case overreach.

## Changelog

| Date | Version | Change |
|---|---|---|
| `2026-10` | v1 | Initial entry added under the owner-directed corpus expansion |
