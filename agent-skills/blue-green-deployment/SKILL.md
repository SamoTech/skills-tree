---
name: blue-green-deployment
description: Run two production environments and switch traffic between them, so a release becomes a reversible routing change instead of a waiting period for breakage.
metadata:
  source: skills/17-infrastructure/blue-green-deployment.md
  category: 17-infrastructure
  version: "v1"
---

# Blue-Green Deployment

Category: Infrastructure | Level: intermediate | Stability: experimental | Version: v1

## Description

A deployment that mutates the live environment in place makes rollback a race against the damage. This skill keeps two full environments — blue, live, and green, idle — and makes the release a routing flip: the new version deploys to the idle color, is verified there, traffic switches to it, and the old color stays warm for exactly as long as the new one needs to prove itself. Rollback is then the same switch in the other direction, which is what makes the flip a decision rather than a gamble.

## When to Use

Use for stateless or forward-compatible services where a full second environment is affordable and a fast, reversible cutover is worth the cost.

Do not blue-green around breaking database changes: if the old color cannot run on the new schema, the switch is not reversible and the pattern is theater.

## Inputs

| Input | Type | Required | Description |
|---|---|---|---|
| `release` | `record` | Yes | The version being deployed to the idle environment |
| `routing` | `switch` | Yes | The traffic control between the two environments |
| `soak` | `duration` | Yes | How long the old environment stays warm after the flip |

## Procedure

1. Keep two environments, with the idle one always ready to receive the next release.
2. Deploy the new version to the idle color only, and verify it there — health, smoke, readiness — while production is untouched.
3. Flip routing to the new color, gradually or at once by design, and watch the user-visible symptoms rather than the deploy logs.
4. Keep the old color warm for the soak period: rollback during soak is a routing change, measured in seconds.
5. Handle state carefully: the schema and its consumers must be forward-compatible with both colors, or the flip is one-way.
6. Retire the old version after soak, and immediately prepare the idle color for the next release — the pattern only works while it is always two environments.

## Outputs

| Output | Type | Description |
|---|---|---|
| `cutover` | `record` | The flip with time, direction, and verification evidence |
| `rollback` | `plan` | The reverse switch, ready during the entire soak |

## Runnable Example

```python
class Router:
    def __init__(self):
        self.live = "blue"
        self.versions = {"blue": "v1.2.9", "green": None}

    def idle(self):
        return "green" if self.live == "blue" else "blue"

    def deploy(self, version):
        self.versions[self.idle()] = version

    def flip(self):
        self.live = self.idle()

router = Router()
router.deploy("v1.3.0")
print("live:", router.live, "idle holds:", router.versions[router.idle()])
router.flip()
print("live:", router.live, "rollback target:", router.versions["blue"])
```

## Failure Modes

| Failure Mode | Cause | Mitigation |
|---|---|---|
| In-place drift | The idle environment quietly becoming non-redeployable | Rehearse deploys to the idle color regularly |
| One-way schema | A migration the old color cannot survive | Forward-compatible schema changes before the flip |
| Instant retirement | The old version destroyed before the soak ends | Keep the old color warm for the full soak |
| Verification in production | Testing deferred until after the flip | Verify on the idle color before switching |
| Stateful split | Session state trapped on the wrong color | Externalize state or drain sessions before the flip |

## Security and Authority Boundary

The routing switch is a security boundary: whoever can flip traffic between environments can redirect production, so route changes require the same authorization and audit as production deploys, and the idle environment must hold production data protections even while idle.

## Evidence

This skill is grounded in dated public implementation references:

1. Martin Fowler's article on blue-green deployment (https://martinfowler.com/bliki/BlueGreenDeployment.html).
2. Wikipedia's overview of blue-green deployment (https://en.wikipedia.org/wiki/Blue-green_deployment).

Honest boundary: these are implementation references, not adoption or demand evidence; this entry was added under the owner-directed corpus expansion recorded in `meta/memory/DECISIONS.md`, and no demand signal is claimed for it.

## Related Skills

- [Deployment Rollback](deployment-rollback.md) — the reversal blue-green makes cheap.
- [Container Image Tagging](container-image-tagging.md) — the immutable artifacts each color runs.

## Changelog

| Date | Version | Change |
|---|---|---|
| `2026-10` | v1 | Initial entry added under the owner-directed corpus expansion |
