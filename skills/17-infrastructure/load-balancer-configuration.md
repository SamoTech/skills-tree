---
title: "Load Balancer Configuration"
category: 17-infrastructure
level: intermediate
stability: experimental
description: "Configure load balancers for distribution algorithm, health checking, session handling, and TLS termination, with capacity limits and drain behavior verified before production traffic."
added: "2026-10"
version: v1
related: ["health-check-endpoints","blue-green-deployment"]
---

# Load Balancer Configuration

Category: Infrastructure | Level: intermediate | Stability: experimental | Version: v1

## Description

A load balancer decides who receives traffic and who gets cut off when things go wrong. The skill covers choosing the distribution strategy deliberately, wiring health checks that fail toward the safe side, handling session affinity or stickiness only when the application requires it, terminating TLS with managed certificates, and setting connection limits that protect backends. Every configuration is verified with synthetic traffic before production cutover.

## When to Use

Use when traffic must be distributed across multiple application instances, or when an existing balancer misroutes, cuts healthy backends, or overloads them.

Do not copy a health check from a template without confirming the response semantics. A check that returns success on an overloaded backend removes the balancer’s ability to protect it.

## Inputs

| Input | Type | Required | Description |
|---|---|---|---|
| `backends` | `table` | Yes | Backend pool with capacity, protocol, and health endpoints |
| `strategy` | `enum` | No | Distribution: `round-robin` (default), `least-connections`, or `ip-hash` |
| `tls` | `object` | No | Certificate source and termination policy |

## Procedure

1. Define the backend pool with real capacity figures, protocols, and health endpoints.
2. Select the distribution strategy deliberately; affinity only with an application reason.
3. Configure health checks with thresholds tuned to fail toward removing a backend.
4. Set connection limits sized to the weakest backend, not the strongest.
5. Terminate TLS per policy with certificate renewal handled before expiry.
6. Verify with synthetic traffic: distribution, failover, and drain behavior, before cutover.

## Outputs

| Output | Type | Description |
|---|---|---|
| `lb_config` | `object` | Applied balancer configuration with strategy and limits |
| `verification_report` | `table` | Distribution, failover, and drain test results |
| `capacity_notes` | `object` | Per-backend limits and the sizing rationale |

## Runnable Example

```python
def simulate_round_robin(backends, requests):
    """backends: [name]; returns per-backend counts"""
    counts = {b: 0 for b in backends}
    for i in range(requests):
        counts[backends[i % len(backends)]] += 1
    return counts

def simulate_failover(backends, dead, requests):
    live = [b for b in backends if b not in dead]
    return simulate_round_robin(live, requests)

print(simulate_round_robin(["app-1", "app-2", "app-3"], 9))
print(simulate_failover(["app-1", "app-2", "app-3"], ["app-2"], 9))
```

## Failure Modes

| Failure Mode | Cause | Mitigation |
|---|---|---|
| Healthy backend cut | Health check misreads the readiness path | Test checks against real overload conditions |
| Overload funneled | Limits sized to the strongest backend | Size limits to the weakest member |
| Session breakage | Affinity disabled for a session-bound app | Enable stickiness only where required and document it |
| Certificate expiry | Renewal not automated | Managed renewal with alerting before expiry |
| Drain surprise | Connections dropped at cutover | Verify graceful drain in the pre-production test |

## Security and Authority Boundary

The balancer is an availability chokepoint. Restrict configuration access, prefer managed certificates over pasted ones, and log routing changes, because an unnoticed misroute is indistinguishable from an outage until someone reads the balancer.

## Evidence

This skill is grounded in dated public implementation references:

1. The HAProxy load balancer documentation (https://www.haproxy.org/).
2. The Kubernetes ingress documentation for cluster-level traffic distribution (https://kubernetes.io/docs/concepts/services-networking/ingress/).

Honest boundary: these are implementation references, not adoption or demand evidence; this entry was added under the owner-directed corpus expansion recorded in `meta/memory/DECISIONS.md`, and no demand signal is claimed for it.

## Related Skills

- [Health Check Endpoints](health-check-endpoints.md) — the readiness signals the balancer routes on.
- [Blue-Green Deployment](blue-green-deployment.md) — the cutover pattern that relies on balancer switching.

## Changelog

| Date | Version | Change |
|---|---|---|
| `2026-10` | v1 | Initial entry added under the owner-directed corpus expansion |
