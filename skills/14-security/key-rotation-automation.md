---
title: "Key Rotation Automation"
category: 14-security
level: intermediate
stability: experimental
description: "Automate cryptographic key and credential rotation across services with dual-key overlap, staged rollout, and telemetry-verified revocation, eliminating long-lived shared secrets."
added: "2026-10"
version: v1
related: ["secrets-management","audit-logging"]
---

# Key Rotation Automation

Category: Security | Level: intermediate | Stability: experimental | Version: v1

## Description

Rotation fails when it breaks production or when the old key survives. The skill covers inventorying keys and their dependents, rotating with dual-key overlap so consumers migrate without downtime, staging rollout by dependency order, then revoking the old key only after verifying zero usage. Every step is driven by measured telemetry, not calendar optimism.

## When to Use

Use when long-lived keys and credentials must be replaced on a schedule or after exposure, across services that cannot all be updated atomically.

Do not rotate by deleting the old key and hoping. Without usage telemetry and overlap, rotation becomes an outage with a security rationale.

## Inputs

| Input | Type | Required | Description |
|---|---|---|---|
| `key_inventory` | `table` | Yes | Keys with type, scope, age, and dependent services |
| `usage_telemetry` | `table` | Yes | Per-key usage counts over a recent window |
| `policy` | `object` | No | Rotation interval, overlap period, and staging order |

## Procedure

1. Inventory every key with its scope, dependents, and last-rotation date.
2. Generate the replacement and publish it alongside the old key as dual-active.
3. Migrate dependents in dependency order, verifying each accepts the new key.
4. Watch usage telemetry until the old key shows zero uses over the overlap window.
5. Revoke the old key and record the revocation evidence.
6. Alert on any key that exceeds its rotation interval or shows anomalous usage.

## Outputs

| Output | Type | Description |
|---|---|---|
| `rotation_record` | `table` | Per-key rotation history with overlap and revocation evidence |
| `stale_keys` | `list` | Keys past their rotation interval or unused and revocable |
| `rollback_plan` | `object` | How to restore the previous key if a consumer breaks |

## Runnable Example

```python
def plan_rotation(keys, telemetry, interval=90):
    """keys: {key: age_days}; telemetry: {key: [daily uses]}"""
    plan = []
    for key, age in keys.items():
        uses = telemetry.get(key, [])
        recent_zero = len(uses) >= 2 and uses[-1] == 0 and uses[-2] == 0
        if recent_zero:
            plan.append({"key": key, "action": "revoke", "reason": "unused through overlap"})
        elif age > interval:
            plan.append({"key": key, "action": "rotate", "reason": "age over interval"})
        else:
            plan.append({"key": key, "action": "keep"})
    return plan

print(plan_rotation(
    {"db-prod": 120, "ci-runner": 40, "legacy-svc": 30},
    {"db-prod": [5, 3], "ci-runner": [10, 12], "legacy-svc": [0, 0]},
))
```

## Failure Modes

| Failure Mode | Cause | Mitigation |
|---|---|---|
| Rotation outage | Old key revoked before consumers migrated | Dual-active overlap gated by usage telemetry |
| Zombie keys | Revoked key still cached by a service | Verify zero usage over the window before revoking |
| Inventory gaps | Key unknown to the inventory never rotates | Discover keys by scanning config and secrets stores |
| New key weaker | Generated with deprecated parameters | Generate to current policy and verify before publishing |
| Emergency break-glass confusion | Rotation lands during an incident | Freeze rotations during active incidents |

## Security and Authority Boundary

Rotation automation holds privileged access. Keep new keys in a secrets manager with scoped, short-lived credentials where possible, log every rotation and revocation for audit, and gate revocation on telemetry so emergency rollback remains possible.

## Evidence

This skill is grounded in dated public implementation references:

1. The NIST key management recommendations (https://csrc.nist.gov/pubs/sp/800/57/pt1/r5/final).
2. The HashiCorp Vault secrets management system (https://github.com/hashicorp/vault).

Honest boundary: these are implementation references, not adoption or demand evidence; this entry was added under the owner-directed corpus expansion recorded in `meta/memory/DECISIONS.md`, and no demand signal is claimed for it.

## Related Skills

- [Secrets Management](secrets-management.md) — the storage and scoping layer rotated keys live in.
- [Audit Logging](audit-logging.md) — the evidence trail every rotation and revocation writes.

## Changelog

| Date | Version | Change |
|---|---|---|
| `2026-10` | v1 | Initial entry added under the owner-directed corpus expansion |
