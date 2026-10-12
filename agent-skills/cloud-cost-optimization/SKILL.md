---
name: cloud-cost-optimization
description: Reduce cloud spend by right-sizing resources, eliminating idle capacity, selecting pricing models, and attributing costs per service, with savings verified after every change rather than assumed.
metadata:
  source: skills/17-infrastructure/cloud-cost-optimization.md
  category: 17-infrastructure
  version: "v1"
---

# Cloud Cost Optimization

Category: Infrastructure | Level: intermediate | Stability: experimental | Version: v1

## Description

Cost optimization is an engineering loop, not a cleanup day. The skill covers attributing spend to services with allocation tags, finding waste by comparing provisioned to observed peak utilization, right-sizing with headroom rules, committing predictable steady load to reserved or committed-use pricing, and verifying each change against the bill after it lands. Savings are measured in the billing data or they are claimed nowhere.

## When to Use

Use when cloud spend must be reduced or held flat against growth, or when bills rise without a clear attribution of the increase.

Do not cut capacity without observing utilization peaks first. An oversized instance is waste; a right-sized-away headroom is an outage with a monthly line item.

## Inputs

| Input | Type | Required | Description |
|---|---|---|---|
| `billing_data` | `table` | Yes | Per-resource spend with service and tag attribution |
| `utilization_metrics` | `table` | Yes | Observed peak utilization for provisioned resources |
| `commitment_options` | `table` | No | Reserved and committed-use pricing available for steady load |

## Procedure

1. Attribute all spend to services through allocation tags before optimizing anything.
2. Find waste: resources with observed peaks far below provisioned capacity.
3. Right-size against peak utilization with an explicit headroom rule, never averages.
4. Match pricing models to load shape: commitments for steady, on-demand for spiky.
5. Schedule or automate idle capacity, such as off-hours dev environments.
6. Verify every change against the next billing cycle and record realized savings.

## Outputs

| Output | Type | Description |
|---|---|---|
| `attribution_report` | `table` | Spend per service and tag with anomalies flagged |
| `optimization_plan` | `list` | Changes ranked by expected savings, with headroom rationale |
| `savings_ledger` | `table` | Realized savings per change, verified against bills |

## Runnable Example

```python
def rightsize(provisioned, observed_peak, headroom=0.3):
    """provisioned/observed in same units; returns new size"""
    needed = observed_peak * (1 + headroom)
    return {"new_size": round(needed, 2), "savings_fraction": round(max(0.0, 1 - needed / provisioned), 3)}

print(rightsize(provisioned=16, observed_peak=4))
print(rightsize(provisioned=16, observed_peak=13))
```

## Failure Modes

| Failure Mode | Cause | Mitigation |
|---|---|---|
| Unattributed spend | Resources without tags bill to a mystery bucket | Tag policy enforced before optimization |
| Headroom cut too thin | Right-sized away the safety margin | Peak-based sizing with an explicit headroom rule |
| Commitment lock-in | Steady discount bought for spiky load | Match commitment only to demonstrably steady usage |
| Savings claimed, not verified | Estimates reported as wins | Verify against billing data after every change |
| Optimization by deletion | Idle-looking resources that are standby capacity | Confirm purpose before removing any resource |

## Security and Authority Boundary

Cost dashboards expose system topology and business volume. Keep attribution data internal, be careful exporting billing detail to third-party tools, and never let optimization scripts delete resources without an approval path, because some waste-shaped resources are load-bearing.

## Evidence

This skill is grounded in dated public implementation references:

1. The AWS cost management services overview (https://aws.amazon.com/aws-cost-management/).
2. The Finops Foundation practices for cloud financial management (https://www.finops.org/).

Honest boundary: these are implementation references, not adoption or demand evidence; this entry was added under the owner-directed corpus expansion recorded in `meta/memory/DECISIONS.md`, and no demand signal is claimed for it.

## Related Skills

- [Capacity Planning](capacity-planning.md) — the headroom discipline that keeps right-sizing safe.
- [Alerting Design](alerting-design.md) — the monitoring that proves right-sized systems still perform.

## Changelog

| Date | Version | Change |
|---|---|---|
| `2026-10` | v1 | Initial entry added under the owner-directed corpus expansion |
