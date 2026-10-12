---
name: declarative-infrastructure
description: Define infrastructure as reviewed, versioned code — desired state, applied by a controller — so environments are reproducible, diffable, and rebuildable from source alone.
metadata:
  source: skills/17-infrastructure/declarative-infrastructure.md
  category: 17-infrastructure
  version: "v1"
---

# Declarative Infrastructure

Category: Infrastructure | Level: intermediate | Stability: experimental | Version: v1

## Description

Infrastructure described imperatively is infrastructure nobody can rebuild: the console clicks that made it exist live in a browser history. This skill makes the desired state the source of truth: resources are declared in code, the code is reviewed and versioned, and a reconciler applies the declaration — reporting a diff between what exists and what is wanted before it changes anything. The payoff is that the environment is no longer a memory; it is a file, with a history, that can be recreated in another region on a bad day.

## When to Use

Use for any environment expected to outlive a single change — clusters, databases, networks, queues — and for anything that must be rebuilt identically elsewhere.

Do not drive one-off break-glass resources through the declarative pipeline during an incident; make the manual change, record it, and reconcile the declaration afterward.

## Inputs

| Input | Type | Required | Description |
|---|---|---|---|
| `declaration` | `code` | Yes | The desired state expressed as reviewed infrastructure code |
| `state` | `map` | Yes | The recorded actual state the controller reconciles against |
| `plan` | `diff` | Yes | The preview of changes between current and desired |

## Procedure

1. Declare desired state in code — resources, parameters, and their relations — with nothing that exists only as a console change.
2. Store the declaration in version control with review, so every infrastructure change has an author, a diff, and a reason.
3. Preview before applying: generate the plan and read it, because the apply step is where the diff meets production.
4. Apply through the reconciler, and let it record state — never mutate resources by hand where the controller watches them.
5. Treat drift as an incident: a manual change to a managed resource gets reconciled or recorded, not ignored.
6. Rehearse the rebuild: a declaration that has never created a fresh environment is a hypothesis, not a backup.

## Outputs

| Output | Type | Description |
|---|---|---|
| `plan` | `diff` | The proposed changes between recorded and desired state |
| `applied_state` | `map` | What the controller created, changed, or destroyed |
| `drift_report` | `map` | Divergences between declaration and reality |

## Runnable Example

```python
DESIRED = {
    "queue": {"name": "events", "retention_days": 7},
    "bucket": {"name": "reports", "versioned": True},
}

def plan(current, desired):
    changes = {}
    for key, want in desired.items():
        have = current.get(key)
        if have is None:
            changes[key] = {"action": "create", "value": want}
        elif have != want:
            changes[key] = {"action": "update", "from": have, "to": want}
    for key in current:
        if key not in desired:
            changes[key] = {"action": "delete"}
    return changes

current = {"queue": {"name": "events", "retention_days": 30}}
print(plan(current, DESIRED))
```

## Failure Modes

| Failure Mode | Cause | Mitigation |
|---|---|---|
| Console drift | Manual edits silently diverging from the declaration | Detect drift and reconcile or record every divergence |
| Apply-without-plan | Changes hitting production unread | Always generate and read the plan first |
| Hand-edited state | State files mutated into folklore | Never hand-edit state; act through the reconciler |
| Unreviewed changes | Infrastructure edited like scratch config | Same review bar as application code |
| Unrehearsed rebuilds | The declaration has never built a fresh environment | Rehearse a clean rebuild periodically |

## Security and Authority Boundary

Infrastructure code holds the shape of the estate and often the references to its most sensitive stores: declarations must be reviewed with the same scrutiny as application code, secrets referenced by identity rather than embedded, and reconciler credentials guarded as the master key to every resource it can create.

## Evidence

This skill is grounded in dated public implementation references:

1. The Terraform documentation on infrastructure as code (https://developer.hashicorp.com/terraform/docs).
2. Wikipedia's overview of infrastructure as code (https://en.wikipedia.org/wiki/Infrastructure_as_code).

Honest boundary: these are implementation references, not adoption or demand evidence; this entry was added under the owner-directed corpus expansion recorded in `meta/memory/DECISIONS.md`, and no demand signal is claimed for it.

## Related Skills

- [Kubernetes Deployment](kubernetes-deployment.md) — a controller-managed runtime this pattern provisions.
- [Container Image Tagging](container-image-tagging.md) — the immutable artifacts declarations pin.

## Changelog

| Date | Version | Change |
|---|---|---|
| `2026-10` | v1 | Initial entry added under the owner-directed corpus expansion |
