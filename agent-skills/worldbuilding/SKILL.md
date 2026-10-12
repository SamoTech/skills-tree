---
name: worldbuilding
description: Construct fictional settings as an explicit fact ledger with category constraints and mechanical consistency checks so a story world stays coherent as it grows.
metadata:
  source: skills/13-creative/worldbuilding.md
  category: 13-creative
  version: "v1"
---

# Worldbuilding

Category: Creative | Level: intermediate | Stability: experimental | Version: v1

## Description

A fictional world breaks the moment its facts disagree: the bridge was built two centuries after the plague it preceded. This skill treats worldbuilding as a ledger — every established fact recorded once, with dates, places, and in-world sources — plus mechanical checks that new material does not contradict the record. The ledger is the artifact; prose merely cites it.

## When to Use

Use when creating or extending a fictional setting — for novels, games, or campaigns — that will outlive a single writing session and must remain internally consistent.

Do not use for improvisational settings that exist for one scene; a ledger for throwaway fiction is overhead, not value.

## Inputs

| Input | Type | Required | Description |
|---|---|---|---|
| `facts` | `map[name -> record]` | Yes | The established fact ledger with dates and sources |
| `draft` | `list[(name, value)]` | Yes | New material proposed for the ledger |
| `constraints` | `list[rule]` | No | Category rules, e.g. event ordering or population bounds |

## Procedure

1. Record every accepted fact exactly once with its in-world date, location, and the source that established it.
2. Check every draft fact against the ledger before it is accepted; contradictions are reported with both records.
3. Encode ordering constraints between dated events so chronology is checked mechanically, not by memory.
4. Prefer reconciling a contradiction over retconning silently; when a retcon is chosen, record it as a new ledger entry.
5. Keep the ledger versioned with the work so any chapter can be traced to the world state it was written against.
6. Leave gaps explicitly marked as unknown; unrecorded is not the same as unrestricted.

## Outputs

| Output | Type | Description |
|---|---|---|
| `ledger` | `map[name -> record]` | The updated fact ledger |
| `contradictions` | `list[(name, recorded, proposed)]` | Draft facts that conflict with the ledger |

## Runnable Example

```python
def check_timeline(draft, known_years):
    """Flag draft events whose years contradict the recorded ledger."""
    contradictions = []
    for name, year in draft:
        if name in known_years and known_years[name] != year:
            contradictions.append((name, known_years[name], year))
    return contradictions

known_years = {"great bridge built": 1200, "second age begins": 1350}
draft = [("great bridge built", 1200), ("second age begins", 1250), ("plague of ash", 1401)]
print(check_timeline(draft, known_years))
```

## Failure Modes

| Failure Mode | Cause | Mitigation |
|---|---|---|
| Chronology drift | Dates held in memory across chapters | Record every dated fact in the ledger and check drafts |
| Silent retcons | Old facts rewritten without a record | Log every retcon as its own ledger entry |
| Fact duplication | One event recorded with two dates | Key facts by a single canonical name |
| Unbounded invention | New material contradicts category rules | Check drafts against recorded constraints |
| False gaps | Unknown mistaken for unrecorded | Mark unknowns explicitly in the ledger |

## Security and Authority Boundary

Fictional worlds can contain real patterns worth protecting: place names, cultures, and communities borrowed from reality deserve respectful, researched use, and the ledger documents provenance so inherited material is cited, not erased.

## Evidence

This skill is grounded in dated public implementation references:

1. Wikipedia’s overview of worldbuilding (https://en.wikipedia.org/wiki/Worldbuilding).
2. Wikipedia’s overview of fiction as a narrative form (https://en.wikipedia.org/wiki/Fiction).

Honest boundary: these are implementation references, not adoption or demand evidence; this entry was added under the owner-directed corpus expansion recorded in `meta/memory/DECISIONS.md`, and no demand signal is claimed for it.

## Related Skills

- [Creative Writing](creative-writing.md) — the prose craft that cites this ledger rather than re-deriving the world.
- [Game Level Design](game-level-design.md) — interactive spaces whose layouts must respect the same ledger.

## Changelog

| Date | Version | Change |
|---|---|---|
| `2026-10` | v1 | Initial entry added under the owner-directed corpus expansion |
