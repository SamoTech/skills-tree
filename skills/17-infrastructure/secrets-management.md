---
title: "Secrets Management"
category: 17-infrastructure
level: intermediate
stability: experimental
description: "Store and deliver credentials through a managed system — never in code or config files — with scoped leases, rotation, and audit, so a leak has a blast radius and an end date."
added: "2026-10"
version: v1
related: ["kubernetes-deployment", "dependency-auditor"]
---

# Secrets Management

Category: Infrastructure | Level: intermediate | Stability: experimental | Version: v1

## Description

A credential in a config file is a credential in a repository, a backup, and a log shipper forever. This skill routes around that: secrets live in a dedicated store, workloads fetch them at start time under an authenticated identity, each credential carries a scope and a lease, and rotation is routine rather than an incident. The audit trail closes the loop — who fetched what, when, under which role — because the question after a leak is never only what got out, but what it could reach and for how long.

## When to Use

Use for any credential a workload needs — API keys, database credentials, signing material — delivered at runtime by identity, with rotation intervals that limit the lifetime of a stolen value.

Do not build home-grown encryption schemes or stash credentials in environment files that outlive their leak; the managed path exists precisely so the shortcuts do not have to.

## Inputs

| Input | Type | Required | Description |
|---|---|---|---|
| `secret_ref` | `string` | Yes | The logical name the workload requests |
| `identity` | `record` | Yes | The authenticated workload identity making the request |
| `lease` | `map` | Yes | Scope, duration, and renewal policy for the grant |

## Procedure

1. Inventory the credentials first: every secret gets an owner, a scope, and a rotation interval before it gets a store entry.
2. Store values only in the secrets system, addressed by logical name, with no copies in code, config files, or CI variables.
3. Deliver at runtime: the workload authenticates as itself and receives only the entries its scope allows.
4. Lease and rotate: credentials expire by policy, and rotation is a routine operation with a tested procedure, not an emergency.
5. Audit every fetch — identity, secret, time — and route the log somewhere a compromised workload cannot edit.
6. Revoke on suspicion, and drill revocation like backups: a rotation path never exercised will fail exactly when it matters.

## Outputs

| Output | Type | Description |
|---|---|---|
| `grant` | `record` | The scoped, time-bound credential issued to the identity |
| `rotation_log` | `list` | Rotations and revocations with dates and owners |
| `audit_trail` | `list` | Fetch events by identity, secret, and time |

## Runnable Example

```python
class SecretsStore:
    def __init__(self):
        self.entries = {}
        self.leases = {}

    def issue(self, name, value, ttl_seconds):
        self.entries[name] = value
        self.leases[name] = {"ttl": ttl_seconds}

    def fetch(self, name, scopes, now, issued_at):
        lease = self.leases.get(name)
        if lease is None:
            raise KeyError("unknown entry requested")
        if name not in scopes:
            raise PermissionError("identity not scoped for this entry")
        if now - issued_at > lease["ttl"]:
            raise PermissionError("lease expired; rotation required")
        return self.entries[name]

store = SecretsStore()
store.issue("db_credential", "short-lived-grant", ttl_seconds=3600)
scopes = {"db_credential", "cache_url"}
print(store.fetch("db_credential", scopes, now=100, issued_at=0))
```

## Failure Modes

| Failure Mode | Cause | Mitigation |
|---|---|---|
| Config-file credentials | A secret committed, backed up, and shipped in logs | Store by logical name; deliver at runtime only |
| Over-scoped grants | One credential reaching everything it never needed | Scope per identity; least privilege per fetch |
| Eternal credentials | Values that live until the incident that rotates them | Lease and rotate on a fixed interval |
| Unexercised rotation | The rotation path fails during the real event | Drill rotation and revocation routinely |
| Unaudited fetches | No answer to who read what and when | Audit every fetch to an append-only log |

## Security and Authority Boundary

The secrets system is the highest-value target in the estate: its stores must be encrypted at rest, its access decisions must run on workload identity rather than shareable credentials, and its audit logs must live outside the reach of the identities they record.

## Evidence

This skill is grounded in dated public implementation references:

1. The HashiCorp Vault documentation (https://developer.hashicorp.com/vault/docs).
2. The twelve-factor app guidance on configuration and credentials (https://12factor.net/config).

Honest boundary: these are implementation references, not adoption or demand evidence; this entry was added under the owner-directed corpus expansion recorded in `meta/memory/DECISIONS.md`, and no demand signal is claimed for it.

## Related Skills

- [Kubernetes Deployment](kubernetes-deployment.md) — the runtime identity that fetches credentials.
- [Dependency Auditor](dependency-auditor.md) — the pipeline that catches credential leaks in dependencies.

## Changelog

| Date | Version | Change |
|---|---|---|
| `2026-10` | v1 | Initial entry added under the owner-directed corpus expansion |
