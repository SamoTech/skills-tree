---
name: kubernetes-deployment
description: Build a Deployment manifest with pinned image tags, explicit resource requests and limits, distinct readiness and liveness probes, and a declared rollout strategy so container runs stay predictable.
metadata:
  source: skills/17-infrastructure/kubernetes-deployment.md
  category: 17-infrastructure
  version: "v1"
---

# Kubernetes Deployment

Category: Infrastructure | Level: intermediate | Stability: experimental | Version: v1

## Description

A Deployment manifest is where container defaults become incidents: floating tags, unset resource bounds, identical probes, and an implicit rollout strategy. This skill defines the manifest contract: pin the image, declare requests and limits, give readiness and liveness probes distinct purposes, and state the rollout strategy and history bound explicitly.

## When to Use

Use when authoring or reviewing a Kubernetes Deployment manifest for a long-running service.

Do not use for one-off pods, batch Jobs, or StatefulSets; their lifecycle contracts differ and need their own manifests.

## Inputs

| Input | Type | Required | Description |
|---|---|---|---|
| `name` | `string` | Yes | Deployment and label name |
| `image` | `string` | Yes | Fully pinned image reference including registry and tag |
| `replicas` | `integer` | Yes | Desired replica count |
| `resources` | `object` | Yes | CPU and memory requests and limits per container |
| `probes` | `object` | Yes | Distinct readiness and liveness probe definitions |

## Procedure

1. Pin the image to an immutable tag or digest; latest is not a deployable version.
2. Declare resource requests and limits for every container; unbounded containers share fate with their neighbors.
3. Give readiness and liveness probes different purposes and settings; identical probes detect nothing distinct.
4. Set the replica count and the rollout strategy explicitly, including max unavailable and max surge.
5. Configure a bounded revision history so rollback targets exist without growing forever.
6. Match label selectors to the pod template exactly; a mismatch strands replicas unsupervised.
7. Validate the manifest with a dry run before applying; schema errors belong in review, not in apply output.
8. Record the deploy outcome, including revision, conditions, and observed replicas, and compare against the declared intent.

## Outputs

| Output | Type | Description |
|---|---|---|
| `manifest` | `object` | The Deployment manifest conforming to the contract |
| `validation_errors` | `list` | Dry-run rejections with the offending field |
| `revision` | `string` | The rollout revision after apply |
| `rollout_status` | `object` | Observed replicas and conditions versus declared intent |

## Runnable Example

```python
def build_deployment(name, image, replicas, resources, probes):
    """Build a Deployment manifest with a pinned image and explicit bounds."""
    return {
        "apiVersion": "apps/v1",
        "kind": "Deployment",
        "metadata": {"name": name},
        "spec": {
            "replicas": replicas,
            "selector": {"matchLabels": {"app": name}},
            "template": {
                "metadata": {"labels": {"app": name}},
                "spec": {
                    "containers": [
                        {
                            "name": name,
                            "image": image,
                            "resources": resources,
                            "readinessProbe": probes["readiness"],
                            "livenessProbe": probes["liveness"],
                        }
                    ],
                },
            },
        },
    }

manifest = build_deployment(
    "web",
    "registry.internal/web:1.4.2",
    3,
    {
        "requests": {"cpu": "100m", "memory": "128Mi"},
        "limits": {"cpu": "500m", "memory": "512Mi"},
    },
    {
        "readiness": {"httpGet": {"path": "/healthz", "port": 8080}, "initialDelaySeconds": 5},
        "liveness": {"httpGet": {"path": "/live", "port": 8080}, "initialDelaySeconds": 10},
    },
)
print(manifest["spec"]["template"]["spec"]["containers"][0]["image"])
```

## Failure Modes

| Failure Mode | Cause | Mitigation |
|---|---|---|
| Floating tag | The image reference uses latest | Pin the tag or digest |
| Identical probes | Readiness equals liveness | Tune each probe for its distinct purpose |
| No limits | Requests and limits are unset | Declare both requests and limits |
| Selector mismatch | Labels were edited after creation | Match selectors to the pod template exactly |
| Unbounded history | revisionHistoryLimit is unset | Set an explicit history limit |

## Security and Authority Boundary

Applying a Deployment manifest grants authority only within the cluster’s own RBAC. Image registries must be trusted, and credentials are supplied through declared secrets, never in the manifest. The manifest is code: it goes through the same review path as any change, and apply happens through the platform’s normal controls.

## Evidence

This skill is grounded in dated public implementation references:

1. The Kubernetes Deployments documentation (https://kubernetes.io/docs/concepts/workloads/deployments/).
2. The Kubernetes documentation on managing resources for containers (https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/).

Honest boundary: these are implementation references, not adoption or demand evidence; this entry was added under the owner-directed corpus expansion recorded in `meta/memory/DECISIONS.md`, and no demand signal is claimed for it.

## Related Skills

- [IaC Generation](../16-domain-specific/iac-generation.md) — authors infrastructure definitions; this skill constrains the Deployment subset of them.
- [Dockerfile Generation](../05-code/dockerfile-generation.md) — builds the images whose pinned references this manifest consumes.
- [Dependency Auditor](dependency-auditor.md) — surfaces vulnerable image bases the pinning rule must account for.

## Changelog

| Date | Version | Change |
|---|---|---|
| `2026-10` | v1 | Initial entry added under the owner-directed corpus expansion |
