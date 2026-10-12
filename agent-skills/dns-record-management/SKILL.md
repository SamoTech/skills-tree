---
name: dns-record-management
description: Manage DNS records as versioned configuration with TTL strategy, propagation verification, and change safety checks, treating record changes as production deployments with rollback plans.
metadata:
  source: skills/17-infrastructure/dns-record-management.md
  category: 17-infrastructure
  version: "v1"
---

# DNS Record Management

Category: Infrastructure | Level: basic | Stability: experimental | Version: v1

## Description

DNS is the first link in every request path, and its failure modes are slow and confusing. The skill covers expressing records as versioned configuration, choosing TTLs deliberately as a trade between change speed and resolver load, pre-validating changes against the existing zone, applying with a rollback plan, and verifying propagation from independent resolvers rather than assuming it. Record changes follow production discipline because a mistake here takes down everything.

## When to Use

Use when zones and records must be created, modified, or migrated, or when DNS changes need controlled rollout and verification.

Do not lower a TTL and change the record in the same step. The sequence is: lower the TTL, wait out the old TTL, then change the record.

## Inputs

| Input | Type | Required | Description |
|---|---|---|---|
| `zone_state` | `object` | Yes | Current zone records as fetched from the authoritative source |
| `change_set` | `table` | Yes | Record additions, updates, and deletions to apply |
| `ttl_policy` | `object` | No | TTL defaults and the change-speed trade-off per record type |

## Procedure

1. Fetch the current zone state from the authoritative source and record it as the rollback point.
2. Validate the change set: conflicting records, CNAME exclusivity, and target reachability.
3. Apply the TTL strategy: lower before risky changes, restore after verification.
4. Apply changes in dependency order, with service-critical records last when migration allows.
5. Verify propagation from independent resolvers until all answer consistently.
6. Archive the applied state and confirm monitoring reflects the new topology.

## Outputs

| Output | Type | Description |
|---|---|---|
| `applied_zone` | `object` | Zone state after the change, archived with the change record |
| `propagation_report` | `table` | Resolver-by-resolver verification results |
| `rollback_plan` | `object` | Exact steps to restore the pre-change zone state |

## Runnable Example

```python
def check_cname_conflicts(existing, change_set):
    """existing: {name: type}; change_set: [(name, type, action)]"""
    issues = []
    for name, rtype, action in change_set:
        if action == "add" and rtype == "CNAME" and name in existing and existing[name] != "CNAME":
            issues.append({"name": name, "rule": "CNAME coexists with " + existing[name]})
    return {"ok": not issues, "issues": issues}

print(check_cname_conflicts(
    {"api.example.com": "A"},
    [("api.example.com", "CNAME", "add"), ("www.example.com", "CNAME", "add")],
))
```

## Failure Modes

| Failure Mode | Cause | Mitigation |
|---|---|---|
| TTL-change collision | Record changed before the old TTL expired | Sequence: lower TTL, wait, change, restore |
| CNAME exclusivity broken | CNAME added beside other records | Validate the change set against zone rules |
| Assumed propagation | Verified only from the local resolver | Query independent resolvers before declaring done |
| Missing rollback | No archived pre-change state | Record the authoritative state before applying |
| Stale delegation | Zone migration left half the NS set behind | Verify delegation glue and NS records end to end |

## Security and Authority Boundary

DNS control is domain control: a compromised zone can redirect every service, including login flows. Keep zone configuration in version control with review, restrict API credentials tightly, enable change auditing, and treat delegation changes with the same care as certificate authority changes.

## Evidence

This skill is grounded in dated public implementation references:

1. The MDN glossary entry on DNS (https://developer.mozilla.org/en-US/docs/Glossary/DNS).
2. The Internet Systems Consortium, home of the BIND name server (https://www.isc.org/).

Honest boundary: these are implementation references, not adoption or demand evidence; this entry was added under the owner-directed corpus expansion recorded in `meta/memory/DECISIONS.md`, and no demand signal is claimed for it.

## Related Skills

- [Declarative Infrastructure](declarative-infrastructure.md) — the configuration-as-code discipline zone files follow.
- [Health Check Endpoints](health-check-endpoints.md) — the post-change verification that confirms traffic lands correctly.

## Changelog

| Date | Version | Change |
|---|---|---|
| `2026-10` | v1 | Initial entry added under the owner-directed corpus expansion |
