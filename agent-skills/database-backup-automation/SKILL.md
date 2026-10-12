---
name: database-backup-automation
description: Automate database backups with declared retention, restore verification, and encryption, treating a backup as real only after a monitored restore test proves it usable.
metadata:
  source: skills/17-infrastructure/database-backup-automation.md
  category: 17-infrastructure
  version: "v1"
---

# Database Backup Automation

Category: Infrastructure | Level: intermediate | Stability: experimental | Version: v1

## Description

A backup that has never been restored is a hope, not a backup. The skill covers scheduling full and incremental backups with a retention policy that survives audit, encrypting and off-siting them, and, decisively, restoring on a schedule into an isolated environment to verify the backup is complete, current, and usable. Every backup run reports duration, size, and integrity; every restore test reports recovery time against the recovery objectives.

## When to Use

Use when production databases need scheduled, verifiable backups with retention and off-site copies, or when an existing backup routine has never been restore-tested.

Do not declare backup coverage from successful backup jobs alone. Unrestored backups fail at the worst possible moment, usually for silent corruption or version drift reasons.

## Inputs

| Input | Type | Required | Description |
|---|---|---|---|
| `database` | `object` | Yes | Target database with size, engine, and change rate |
| `policy` | `object` | Yes | Schedule, retention tiers, and recovery objectives |
| `restore_env` | `object` | Yes | Isolated environment for scheduled restore verification |

## Procedure

1. Define the policy: full and incremental cadence, retention tiers, and recovery time and point objectives.
2. Run backups on schedule, recording duration, size, checksum, and completion status.
3. Encrypt backups at rest and in transit, and copy them off-site per policy.
4. Prune expired backups per retention tiers and log what was removed.
5. Restore on schedule into the isolated environment and verify completeness and usability.
6. Report measured recovery time against the objective and alert on drift.

## Outputs

| Output | Type | Description |
|---|---|---|
| `backup_log` | `table` | Runs with size, duration, checksum, and status |
| `restore_test_report` | `object` | Latest restore verification with recovery time measured |
| `retention_state` | `object` | Backups held per tier and prune history |

## Runnable Example

```python
def verify_restore(recovery_time_min, rto_min, integrity_ok, fresh_days, max_fresh):
    ok = integrity_ok and recovery_time_min <= rto_min and fresh_days <= max_fresh
    reasons = []
    if not integrity_ok:
        reasons.append("integrity check failed")
    if recovery_time_min > rto_min:
        reasons.append(f"recovery time {recovery_time_min}m exceeds RTO {rto_min}m")
    if fresh_days > max_fresh:
        reasons.append(f"backup age {fresh_days}d exceeds target {max_fresh}d")
    return {"verified": ok, "reasons": reasons}

print(verify_restore(recovery_time_min=42, rto_min=60, integrity_ok=True, fresh_days=1, max_fresh=7))
print(verify_restore(recovery_time_min=95, rto_integrity=None, integrity_ok=False, fresh_days=9, max_fresh=7))
```

## Failure Modes

| Failure Mode | Cause | Mitigation |
|---|---|---|
| Unrestorable backup discovered late | Restore never tested until needed | Scheduled restore verification in an isolated environment |
| Silent corruption | Bit rot in stored backup files | Checksums on write and on restore |
| Retention breach | Old backups kept or pruned wrongly | Tiered retention with prune logging and audit |
| Credential exposure | Backup encryption keys mishandled | Key management separated from backup storage |
| Version drift | Restore target newer or older than backup format | Test with the engine version used in production |

## Security and Authority Boundary

Backups concentrate the entire database, so they inherit and exceed its sensitivity. Encrypt at rest and in transit, store keys separately from backups, restrict restore-environment access, and log every backup and restore operation for audit.

## Evidence

This skill is grounded in dated public implementation references:

1. The PostgreSQL backup and restore documentation (https://www.postgresql.org/docs/current/backup.html).
2. The pgBackRest dedicated PostgreSQL backup and restore tool (https://github.com/pgbackrest/pgbackrest).

Honest boundary: these are implementation references, not adoption or demand evidence; this entry was added under the owner-directed corpus expansion recorded in `meta/memory/DECISIONS.md`, and no demand signal is claimed for it.

## Related Skills

- [Secrets Management](secrets-management.md) — the key custody layer encrypted backups depend on.
- [Deployment Rollback](deployment-rollback.md) — the recovery flow that consumes verified backups.

## Changelog

| Date | Version | Change |
|---|---|---|
| `2026-10` | v1 | Initial entry added under the owner-directed corpus expansion |
