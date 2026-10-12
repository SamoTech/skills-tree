---
title: "Market Research Synthesis"
category: 16-domain-specific
level: intermediate
stability: experimental
description: "Synthesize primary and secondary market research into a decision-ready analysis with sized estimates, source hierarchy, and explicit confidence levels rather than blended opinions."
added: "2026-10"
version: v1
related: ["review-analysis","portfolio-analysis"]
---

# Market Research Synthesis

Category: Domain-Specific | Level: intermediate | Stability: experimental | Version: v1

## Description

Synthesis fails when it averages sources that disagree without explaining why. The skill covers inventorying sources by type and reliability, extracting findings with per-source provenance, reconciling contradictions explicitly rather than blending them, triangulating market sizes from independent methods, and grading each conclusion by the strength of what supports it. The deliverable is a decision memo with a confidence level per claim.

## When to Use

Use when strategy, product, or investment decisions need a consolidated view of a market from mixed primary and secondary sources.

Do not blend conflicting findings into a smoothed average. Contradictions between credible sources are findings, and they get surfaced, not averaged away.

## Inputs

| Input | Type | Required | Description |
|---|---|---|---|
| `sources` | `table` | Yes | Research artifacts with type, date, and methodology notes |
| `questions` | `list` | Yes | The decision questions the synthesis must answer |
| `source_hierarchy` | `object` | No | Reliability ranking by source type for conflict resolution |

## Procedure

1. Inventory sources with type, date, and methodology; discard ones with no traceable method.
2. Extract findings per source with provenance; one row per claim, not per document.
3. Cluster findings against each decision question and surface contradictions.
4. Resolve contradictions with the source hierarchy and record why the loser lost.
5. Triangulate quantitative estimates from at least two independent methods where possible.
6. Grade every conclusion by support strength and state what would change it.

## Outputs

| Output | Type | Description |
|---|---|---|
| `findings_table` | `table` | Claims with source provenance and reliability tier |
| `decision_memo` | `object` | Answers to the decision questions with confidence grades |
| `contradictions` | `list` | Unresolved conflicts and their impact on conclusions |

## Runnable Example

```python
def reconcile(claims, hierarchy):
    """claims: [(source_type, value)]; hierarchy: {source_type: tier 1-3}"""
    if not claims:
        return {"resolved": False, "reason": "no claims"}
    best_tier = min(hierarchy.get(t, 3) for t, _ in claims)
    winners = [(t, v) for t, v in claims if hierarchy.get(t, 3) == best_tier]
    if len({v for _, v in winners}) == 1:
        return {"resolved": True, "value": winners[0][1], "tier": best_tier}
    return {"resolved": False, "reason": "same-tier sources disagree", "candidates": winners}

print(reconcile(
    [("government-census", 1.2), ("vendor-report", 1.9), ("press-release", 2.4)],
    {"government-census": 1, "vendor-report": 3, "press-release": 3},
))
```

## Failure Modes

| Failure Mode | Cause | Mitigation |
|---|---|---|
| Blended contradictions | Averaging conflicting estimates | Resolve via hierarchy or report the contradiction |
| Provenance-free claims | Findings extracted without source links | One provenance row per claim |
| Zombie statistics | Old estimates recycled without dates | Carry the source date with every figure |
| Question drift | Synthesis answers an easier question | Cluster findings against the stated questions |
| False precision | Single-method estimates presented as solid | Triangulate or grade confidence down |

## Security and Authority Boundary

Market research includes paid and confidential data. Respect licensing terms, keep client-confidential findings out of shared artifacts, and attribute figures to sources correctly, because unlicensed reuse of syndicated data carries legal exposure.

## Evidence

This skill is grounded in dated public implementation references:

1. The Wikipedia article on market research as a discipline (https://en.wikipedia.org/wiki/Market_research).
2. The United States Census Bureau public demographic and economic statistics (https://www.census.gov/).

Honest boundary: these are implementation references, not adoption or demand evidence; this entry was added under the owner-directed corpus expansion recorded in `meta/memory/DECISIONS.md`, and no demand signal is claimed for it.

## Related Skills

- [Review Analysis](review-analysis.md) — the qualitative mining layer that feeds synthesis inputs.
- [Portfolio Analysis](portfolio-analysis.md) — the investment-side context synthesis findings must respect.

## Changelog

| Date | Version | Change |
|---|---|---|
| `2026-10` | v1 | Initial entry added under the owner-directed corpus expansion |
