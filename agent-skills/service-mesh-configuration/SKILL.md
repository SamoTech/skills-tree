---
name: service-mesh-configuration
description: Configure service mesh routing, mutual TLS, retries, and traffic policy as declarative configuration with progressive rollout and verifiable policy enforcement between services.
metadata:
  source: skills/17-infrastructure/service-mesh-configuration.md
  category: 17-infrastructure
  version: "v1"
---

# Service Mesh Configuration

Category: Infrastructure | Level: advanced | Stability: experimental | Version: v1

## Description

A mesh moves inter-service policy into a configurable plane, which makes it auditable and also easy to break fleet-wide. The skill covers expressing routing, mutual TLS, and resilience policy declaratively, validating configuration against a running cluster state, rolling it out progressively with traffic verification between steps, and proving enforcement rather than assuming it. Mesh configuration is production security and gets production discipline.

## When to Use

Use when inter-service traffic needs managed routing, encryption, or resilience policy across a fleet of services without rewriting each one.

Do not apply mesh policy fleet-wide in one step. A bad retry or timeout rule is a self-inflicted outage with a single commit.

## Inputs

| Input | Type | Required | Description |
|---|---|---|---|
| `mesh_spec` | `object` | Yes | Declarative routing, mTLS, and resilience policy for the services in scope |
| `services` | `list` | Yes | Workloads the policy applies to, with ownership recorded |
| `rollout` | `object` | No | Progressive stages and verification gates; defaults to staged |

## Procedure

1. Express routing, mutual TLS, and resilience policy as declarative configuration in version control.
2. Validate the configuration: schema, references, and a dry-run against live cluster state.
3. Apply to one service first and verify traffic, latency, and policy enforcement in practice.
4. Progress through stages, verifying enforcement at each gate before expanding scope.
5. Confirm mutual TLS end to end: certificates issued, connections actually encrypted.
6. Record the applied policy state and rollback point for incident response.

## Outputs

| Output | Type | Description |
|---|---|---|
| `applied_policy` | `object` | The mesh configuration now in force, per service |
| `enforcement_report` | `table` | Verified routing, mTLS, and retry behavior per service |
| `rollback_point` | `object` | Last-known-good configuration for fast reversal |

## Runnable Example

```python
def stage_rollout(services, verify):
    """services in order; verify: {service: bool} gate result"""
    applied = []
    for svc in services:
        if not verify.get(svc, False):
            return {"status": "halted", "applied": applied, "failed_at": svc}
        applied.append(svc)
    return {"status": "complete", "applied": applied}

print(stage_rollout(
    ["svc-a", "svc-b", "svc-c"],
    {"svc-a": True, "svc-b": True, "svc-c": False},
))
```

## Failure Modes

| Failure Mode | Cause | Mitigation |
|---|---|---|
| Fleet-wide bad policy | Applied to every namespace at once | Progressive stages with verification gates |
| mTLS assumed, not verified | Certificates issued but connections still plaintext | Verify encryption end to end, per service |
| Retry storms | Aggressive retries amplified an outage | Conservative retry budgets with backoff and caps |
| Config drift | Console edits diverging from version control | Declarative source of truth, regularly reconciled |
| Ownership unknown | No one knows who owns a policy | Record service ownership with the spec |

## Security and Authority Boundary

Mesh policy controls who may talk to whom in production. Keep the configuration in version control with review, enforce mutual TLS as the default posture, and audit policy changes, because the mesh is a privilege-escalation path if its control plane is compromised.

## Evidence

This skill is grounded in dated public implementation references:

1. The Istio service mesh documentation (https://istio.io/).
2. The Linkerd service mesh documentation (https://linkerd.io/).

Honest boundary: these are implementation references, not adoption or demand evidence; this entry was added under the owner-directed corpus expansion recorded in `meta/memory/DECISIONS.md`, and no demand signal is claimed for it.

## Related Skills

- [Kubernetes Deployment](kubernetes-deployment.md) — the workload plane the mesh attaches to.
- [Health Check Endpoints](health-check-endpoints.md) — the signals the rollout gates verify against.

## Changelog

| Date | Version | Change |
|---|---|---|
| `2026-10` | v1 | Initial entry added under the owner-directed corpus expansion |
