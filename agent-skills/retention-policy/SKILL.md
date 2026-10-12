---
name: retention-policy
description: Define and enforce how long each class of stored memory is kept — legal floors, purpose limits, and deletion mechanics — before accumulation becomes liability.
metadata:
  source: skills/03-memory/retention-policy.md
  category: 03-memory
  version: "v1"
---

# Retention Policy

Category: Memory | Level: intermediate | Stability: experimental | Version: v1

## Description

Every stored record is a liability as well as an asset: it ages, it contradicts newer facts, and it answers requests you did not invite. A retention policy decides, per class of memory, how long it is kept, why, and what happens at the boundary. This skill structures that policy — classes, floors, ceilings, deletion mechanics — and keeps the decision explicit instead of the default of keeping everything until something breaks.

## When to Use

Use when an agent persists memory across sessions and operates under privacy obligations, data agreements, or plain hygiene requirements.

Do not apply a single blanket retention to all classes; volatile facts, stable preferences, and legally required records decay on different clocks.

## Inputs

| Input | Type | Required | Description |
|---|---|---|---|
| `classes` | `list` | Yes | Memory categories with their purpose |
| `obligations` | `map` | No | Legal or contractual floors and ceilings per class |
| `mechanics` | `enum` | No | Delete, anonymize, or archive at expiry |

## Procedure

1. Classify stored memory by purpose — operational, preference, legal, diagnostic — because retention hangs on purpose, not on storage technology.
2. For each class, state the ceiling (how long it may be kept) and any floor (how long it must be kept), with the obligation cited.
3. Choose the expiry mechanic per class — hard delete, anonymize, archive — and note that archive is not deletion.
4. Wire expiry into the write path: every record carries its class and expiry, so enforcement is mechanical rather than a periodic cleanup project.
5. Audit enforcement: sample records past expiry and verify the policy ran.
6. Handle deletion requests end-to-end — active store, indexes, backups, and derived artifacts — and record what was out of reach.

## Outputs

| Output | Type | Description |
|---|---|---|
| `policy` | `map` | Per-class floors, ceilings, and mechanics |
| `enforcement` | `map` | Expiry execution status per class |
| `audit` | `list` | Out-of-reach stores and policy violations found |

## Runnable Example

```python
from datetime import date

def apply_retention(records, policy, today):
    kept, actions = [], []
    for r in records:
        rule = policy[r["class"]]
        age_days = (today - r["written"]).days
        if age_days > rule["ceiling_days"]:
            actions.append((r["id"], rule["on_expiry"]))
        else:
            kept.append(r)
    return kept, actions

records = [
    {"id": "d1", "class": "diagnostic", "written": date(2026, 8, 1)},
    {"id": "p1", "class": "preference", "written": date(2026, 10, 1)},
]
policy = {"diagnostic": {"ceiling_days": 30, "on_expiry": "delete"}, "preference": {"ceiling_days": 365, "on_expiry": "delete"}}
print(apply_retention(records, policy, date(2026, 10, 12)))
```

## Failure Modes

| Failure Mode | Cause | Mitigation |
|---|---|---|
| Blanket retention | One duration is applied to every class | Classify by purpose and set per-class rules |
| Missing floors | Legally required records are deleted early | Cite obligations and enforce floors |
| Archive-as-delete | Records are moved somewhere and called gone | State the mechanic honestly |
| Backup blind spot | Deletion never reaches backups or exports | Record what was out of reach |
| No enforcement audit | A policy exists but never runs | Sample past-expiry records and verify |

## Security and Authority Boundary

Retention is the primary lever that limits exposure of personal data: shorter ceilings, purpose-bound classes, and honest mechanics reduce both breach impact and compliance failure. This skill is not legal advice; retention obligations vary by jurisdiction and must be confirmed with counsel where they apply.

## Evidence

This skill is grounded in dated public implementation references:

1. Wikipedia's overview of data retention (https://en.wikipedia.org/wiki/Data_retention).
2. Wikipedia's overview of ISO 8601 date and duration notation used in retention rules (https://en.wikipedia.org/wiki/ISO_8601).

Honest boundary: these are implementation references, not adoption or demand evidence; this entry was added under the owner-directed corpus expansion recorded in `meta/memory/DECISIONS.md`, and no demand signal is claimed for it.

## Related Skills

- [Forgetting](forgetting.md) — the memory-level decision layer feeding this policy.
- [Long-Term Memory](long-term-memory.md) — the durable store whose records this policy bounds.

## Changelog

| Date | Version | Change |
|---|---|---|
| `2026-10` | v1 | Initial entry added under the owner-directed corpus expansion |
