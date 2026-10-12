---
name: customer-churn-analysis
description: Analyze why customers leave by joining behavioral signals with outcomes, scoring churn risk honestly and separating correlation from causation before acting on findings.
metadata:
  source: skills/16-domain-specific/customer-churn-analysis.md
  category: 16-domain-specific
  version: "v1"
---

# Customer Churn Analysis

Category: Domain-Specific | Level: intermediate | Stability: experimental | Version: v1

## Description

Churn analysis is only useful when it changes what a team does next. The skill covers defining churn operationally, joining behavioral signals with observed outcomes, building interpretable risk features, and validating that signals precede churn rather than accompany it. The deliverable is a ranked intervention list with per-signal evidence, plus the honest note that association is not a retention mechanism.

## When to Use

Use when a subscription or recurring-revenue business must understand and predict which customers are likely to leave and why.

Do not treat every correlated metric as a churn cause. Intervening on a signal that merely accompanies churn wastes retention budget and can irritate customers.

## Inputs

| Input | Type | Required | Description |
|---|---|---|---|
| `account_history` | `table` | Yes | Per-account events, usage, and status changes over time |
| `outcome_labels` | `table` | Yes | Observed churn or retention outcomes per account |
| `windows` | `object` | Yes | Feature window and prediction horizon definitions |

## Procedure

1. Define churn operationally: cancellation event, lapse, or inactivity threshold, with the observation window.
2. Join behavioral signals with outcomes using strict temporal windows: features precede the outcome.
3. Build interpretable features: usage trend, support contacts, billing failures, and engagement drop.
4. Score accounts for churn risk with the model kept simple enough to explain per account.
5. Validate that top signals are leading, not coincident, using lagged analysis.
6. Emit a ranked intervention list with per-account evidence and stated confidence.

## Outputs

| Output | Type | Description |
|---|---|---|
| `risk_scores` | `table` | Per-account churn risk with top contributing signals |
| `signal_evidence` | `object` | Per-signal strength and lead time before churn |
| `intervention_list` | `list` | Accounts ranked with suggested actions and caveats |

## Runnable Example

```python
def rank_accounts(accounts):
    """accounts: {id: {usage_slope, support_tickets, failed_payments}}"""
    scored = []
    for aid, a in accounts.items():
        risk = (0.5 * max(0.0, -a["usage_slope"])
                + 0.2 * min(a["support_tickets"] / 5.0, 1.0)
                + 0.3 * min(a["failed_payments"] / 3.0, 1.0))
        scored.append({"id": aid, "risk": round(risk, 3)})
    return sorted(scored, key=lambda x: -x["risk"])

print(rank_accounts({
    "acme": {"usage_slope": -0.4, "support_tickets": 4, "failed_payments": 1},
    "globex": {"usage_slope": 0.1, "support_tickets": 1, "failed_payments": 0},
}))
```

## Failure Modes

| Failure Mode | Cause | Mitigation |
|---|---|---|
| Coincident signals treated as causes | Interventions fired on symptoms | Lag analysis before ranking any signal |
| Churn defined inconsistently | Lapse and inactivity conflated | One operational definition stated up front |
| Feature leakage | Post-churn behavior used as a feature | Enforce the feature window strictly |
| Retention theater | Discounts to accounts that would stay anyway | Target by risk band, not blanket offers |
| Survivor bias in validation | Only completed windows evaluated | Include censored accounts in evaluation |

## Security and Authority Boundary

Churn models segment real customers by behavior. Ensure the data use complies with privacy commitments, do not use protected attributes as features, and keep per-account risk scores need-to-know because they inform commercial decisions about individuals.

## Evidence

This skill is grounded in dated public implementation references:

1. The scikit-learn linear model documentation used for interpretable churn scoring (https://scikit-learn.org/stable/modules/linear_model.html).
2. The Wikipedia article on churn rate as a metric (https://en.wikipedia.org/wiki/Churn_rate).

Honest boundary: these are implementation references, not adoption or demand evidence; this entry was added under the owner-directed corpus expansion recorded in `meta/memory/DECISIONS.md`, and no demand signal is claimed for it.

## Related Skills

- [Review Analysis](review-analysis.md) — the qualitative signal layer where dissatisfaction surfaces first.
- [Cohort Analysis](cohort-analysis.md) — the retention framework churn analysis plugs into.

## Changelog

| Date | Version | Change |
|---|---|---|
| `2026-10` | v1 | Initial entry added under the owner-directed corpus expansion |
