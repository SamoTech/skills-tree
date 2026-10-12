---
name: capacity-planning
description: Forecast infrastructure capacity needs from utilization trends and growth assumptions, producing headroom recommendations with stated assumptions rather than single-point guesses.
metadata:
  source: skills/17-infrastructure/capacity-planning.md
  category: 17-infrastructure
  version: "v1"
---

# Capacity Planning

Category: Infrastructure | Level: intermediate | Stability: experimental | Version: v1

## Description

Capacity planning converts utilization history into headroom decisions. The skill covers measuring current utilization at peak rather than average, projecting demand under explicit growth scenarios, deriving resource needs with target utilization ceilings, and presenting recommendations with the assumptions attached so they can be argued with. The output is a scenario table, not one number, because the honest answer depends on inputs nobody controls.

## When to Use

Use when compute, storage, or network capacity must be provisioned ahead of expected growth, or when recurring saturation needs a structural rather than reactive fix.

Do not plan from average utilization. Peaks are what break systems, and a plan sized to averages fails precisely when it matters.

## Inputs

| Input | Type | Required | Description |
|---|---|---|---|
| `utilization_history` | `table` | Yes | Time series of utilization for each constrained resource |
| `growth_scenarios` | `table` | Yes | Plausible demand scenarios with rates and event shocks |
| `ceilings` | `object` | Yes | Target utilization per resource that triggers scaling |

## Procedure

1. Measure utilization at peak windows per resource, not period averages.
2. Define growth scenarios explicitly: trend, step events, and their probabilities.
3. Project demand per scenario over the planning horizon.
4. Derive required capacity per scenario against the target ceilings.
5. Add headroom for the noisiest scenario and state the chosen margin.
6. Publish the scenario table with assumptions, trigger thresholds, and review dates.

## Outputs

| Output | Type | Description |
|---|---|---|
| `scenario_table` | `table` | Required capacity per resource per scenario |
| `headroom_plan` | `object` | Chosen provisioning with the margin and rationale |
| `trigger_thresholds` | `object` | Utilization alarms that force a plan re-run |

## Runnable Example

```python
def project_capacity(peak_now, growth_rate, horizon_months, ceiling=0.7):
    """peak_now: current peak utilization fraction; growth_rate: monthly"""
    needed = peak_now * ((1 + growth_rate) ** horizon_months)
    provision = needed / ceiling
    return {"peak_needed": round(needed, 3), "provision_fraction": round(provision, 3)}

print(project_capacity(peak_now=0.45, growth_rate=0.10, horizon_months=6))
print(project_capacity(peak_now=0.45, growth_rate=0.25, horizon_months=6))
```

## Failure Modes

| Failure Mode | Cause | Mitigation |
|---|---|---|
| Average-based sizing | Averages hide the peaks that break systems | Size to observed peak windows |
| Single-point forecast | One growth number treated as fact | Scenario table with assumptions stated |
| No trigger thresholds | Plan goes stale until saturation hits | Utilization alarms that force a re-run |
| Hidden coupling missed | One resource sized without its dependencies | Model constrained resources together |
| Correlated demand shocks | Scenarios assume independent growth | Include compound worst cases in the table |

## Security and Authority Boundary

Capacity data reveals system architecture and business growth. Treat utilization and projection artifacts as internal, avoid exposing them in shared dashboards, and provision through the same review discipline as any production change, since headroom decisions are also availability decisions.

## Evidence

This skill is grounded in dated public implementation references:

1. The Wikipedia article on capacity planning (https://en.wikipedia.org/wiki/Capacity_planning).
2. The Kubernetes resource management documentation for requests and limits (https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/).

Honest boundary: these are implementation references, not adoption or demand evidence; this entry was added under the owner-directed corpus expansion recorded in `meta/memory/DECISIONS.md`, and no demand signal is claimed for it.

## Related Skills

- [Alerting Design](alerting-design.md) — the trigger thresholds that keep the plan current.
- [Kubernetes Deployment](kubernetes-deployment.md) — the provisioning plane where headroom lands.

## Changelog

| Date | Version | Change |
|---|---|---|
| `2026-10` | v1 | Initial entry added under the owner-directed corpus expansion |
