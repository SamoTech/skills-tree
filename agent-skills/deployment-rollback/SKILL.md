---
name: deployment-rollback
description: Restore the last known-good release through pre-verified rollback artifacts, recorded migration state, and a rehearsed procedure so a failed deployment recovers within a bounded time budget.
metadata:
  source: skills/17-infrastructure/deployment-rollback.md
  category: 17-infrastructure
  version: "v1"
---

# Deployment Rollback

Category: Infrastructure | Level: advanced | Stability: experimental | Version: v1

## Description

Rollback is a deployment you have already practiced — or a hope. The skill makes it an artifact: the previous release stays deployable, schema migrations carry their compensating steps, the rollback procedure is rehearsed in staging against the same artifact shape, and recovery runs in a defined order with health verification at the end. The measure of success is a bounded recovery time, not the absence of failures.

## When to Use

Use for any release with state — services, migrations, configuration — where reverting to the previous good state must be possible within a stated time budget.

Do not use rollback as the primary deployment strategy; a process that ships failures expecting to revert is a quality problem wearing recovery clothing.

## Inputs

| Input | Type | Required | Description |
|---|---|---|---|
| `current_release` | `map` | Yes | The failing release and its artifacts |
| `last_known_good` | `map` | Yes | The verified previous release, kept deployable |
| `migration_log` | `list[step]` | Yes | Forward migrations with compensating steps |
| `rollback_plan` | `list[ordered step]` | Yes | The rehearsed recovery procedure |

## Procedure

1. Keep the last known-good release deployable — artifacts, configuration, and schema state — until the next one is verified.
2. Record every forward migration with its compensating step; a migration without a reverse is a decision to make rollback impossible.
3. Rehearse the rollback in staging with the same artifacts and order; an unrehearsed plan is a draft.
4. On the failure signal, execute in the recorded order: stop traffic, revert code, revert migrations step by step, restore configuration.
5. Verify health after rollback — probes, smoke checks, error rates — before declaring recovery.
6. Write the incident reference: trigger, release delta, migration state, recovery time against budget.

## Outputs

| Output | Type | Description |
|---|---|---|
| `state` | `rolled_back | blocked` | Whether recovery completed |
| `steps_taken` | `list[(step, verdict)]` | Each rollback step and its verification |
| `recovery_time` | `duration` | Time from signal to verified recovery |

## Runnable Example

```python
def rollback(plan, health_after_step):
    """Execute ordered steps and verify health at the end."""
    taken = []
    for step in plan:
        verdict = "ok" if health_after_step(step) else "failed"
        taken.append((step, verdict))
        if verdict == "failed":
            return "blocked", taken
    return "rolled_back", taken

plan = ["stop-traffic", "revert-code", "revert-migrations", "restore-config"]
good_steps = {"stop-traffic", "revert-code", "revert-migrations", "restore-config"}
print(rollback(plan, lambda step: step in good_steps))
```

## Failure Modes

| Failure Mode | Cause | Mitigation |
|---|---|---|
| No retained artifact | Previous release deleted or unreferenced | Keep the last known good deployable until the next is verified |
| Irreversible migrations | Forward-only schema changes | Record compensating steps with every migration |
| Unrehearsed plan | Rollback procedure written during the outage | Rehearse in staging with real artifacts |
| Config drift | Configuration differs between the two releases | Snapshot and restore configuration with the release |
| Unverified recovery | Traffic restored without health checks | Verify probes and error rates before declaring done |

## Security and Authority Boundary

Rollback restores service state; it does not reconcile data written by the failed release. Data repair, backfills, and customer-impact analysis stay with the data owner after service recovery.

## Evidence

This skill is grounded in dated public implementation references:

1. Wikipedia's overview of blue-green deployment (https://en.wikipedia.org/wiki/Blue-green_deployment).
2. Martin Fowler's note on blue-green deployment (https://martinfowler.com/bliki/BlueGreenDeployment.html).

Honest boundary: these are implementation references, not adoption or demand evidence; this entry was added under the owner-directed corpus expansion recorded in `meta/memory/DECISIONS.md`, and no demand signal is claimed for it.

## Related Skills

- [Kubernetes Deployment](kubernetes-deployment.md) — the deployment mechanics that pin and restore releases.
- [Dependency Auditor](dependency-auditor.md) — dependency evidence that feeds release verification.

## Changelog

| Date | Version | Change |
|---|---|---|
| `2026-10` | v1 | Initial entry added under the owner-directed corpus expansion |
