---
title: "Alerting Design"
category: 17-infrastructure
level: intermediate
stability: experimental
description: "Build alerts around user-visible symptoms and service objectives rather than raw causes, so a page means real impact and silence means real health."
added: "2026-10"
version: v1
related: ["health-check-endpoints", "deployment-rollback"]
---

# Alerting Design

Category: Infrastructure | Level: intermediate | Stability: experimental | Version: v1

## Description

An alert on every metric is a pager that cannot be trusted, and a pager that cannot be trusted gets silenced — usually right before the one that mattered. This skill designs alerting from the top down: start from what users experience, define objectives with error budgets, and alert on the burn rate of those budgets. Cause-level signals become dashboards and debug entries, not pages, because a page is a claim that a human must act now, and every unactionable claim spends trust the system needs for the real ones.

## When to Use

Use whenever a service is on call — user-facing or internal — and especially where pages have grown noisy enough that responders pre-filter them.

Do not page on individual cause metrics with no user-visible symptom; a nearly full disk at three in the morning is a dashboard, not a human.

## Inputs

| Input | Type | Required | Description |
|---|---|---|---|
| `objective` | `record` | Yes | The user-visible service level being protected |
| `burn_rate` | `number` | Yes | How fast the error budget is being consumed |
| `symptom_query` | `query` | Yes | The signal that measures the user experience |

## Procedure

1. Define the objective first — what users experience, measured as availability or latency — before writing a single alert.
2. Alert on burn rate: page when the error budget would exhaust within a bounded window, not on any single bad sample.
3. Keep causes out of the pager: route saturation and dependency signals to dashboards and debug pages, not to humans.
4. Make every page actionable: name the runbook, the owner, and the first command to run, in the alert itself.
5. Review alert performance like code: page rate, action rate, and the fraction of pages that were real become metrics.
6. Retire or repair chatty alerts immediately; a noisy alert is not a safety margin, it is a removed one.

## Outputs

| Output | Type | Description |
|---|---|---|
| `alerts` | `list` | Symptom-based, budget-burning pages with runbooks |
| `review` | `map` | Page rate, action rate, and precision over time |

## Runnable Example

```python
def should_page(burn_rate, window_hours, budget_hours):
    if budget_hours <= 0:
        return False, "no budget defined"
    exhaustion_hours = budget_hours / burn_rate
    if exhaustion_hours < window_hours:
        return True, f"budget exhausts in {exhaustion_hours:.1f} hours"
    return False, "burn within tolerance"

print(should_page(burn_rate=0.5, window_hours=24, budget_hours=8))
print(should_page(burn_rate=4.0, window_hours=24, budget_hours=8))
```

## Failure Modes

| Failure Mode | Cause | Mitigation |
|---|---|---|
| Cause paging | Humans notified of every unhealthy-looking metric | Page on symptoms and budget burn, not causes |
| Unactionable pages | A page with no runbook and no owner | Name the runbook and first step in the alert |
| Alert fatigue | So many pages that real ones get ignored | Retire chatty alerts; measure alert precision |
| Missing objectives | Alerts exist but no user experience is defined | Define the service objective before alerting on it |
| Static thresholds | A fixed line that pages nightly at low traffic | Use burn-rate windows instead of single thresholds |

## Security and Authority Boundary

Alert content travels to the widest, least protected channel in an organization — phones and chat: alert payloads must not embed credentials, internal topology details, or user data, and access to the alerting configuration itself must be protected, because silencing rules are a prime target for an intruder who wants the quiet path.

## Evidence

This skill is grounded in dated public implementation references:

1. The Prometheus alerting documentation (https://prometheus.io/docs/alerting/latest/overview/).
2. The SRE Workbook chapter on alerting on service level objectives (https://sre.google/workbook/alerting-on-slos/).

Honest boundary: these are implementation references, not adoption or demand evidence; this entry was added under the owner-directed corpus expansion recorded in `meta/memory/DECISIONS.md`, and no demand signal is claimed for it.

## Related Skills

- [Health Check Endpoints](health-check-endpoints.md) — the signals symptom alerts consume.
- [Deployment Rollback](deployment-rollback.md) — the action pages most often trigger.

## Changelog

| Date | Version | Change |
|---|---|---|
| `2026-10` | v1 | Initial entry added under the owner-directed corpus expansion |
