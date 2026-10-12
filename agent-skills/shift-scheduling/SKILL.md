---
name: shift-scheduling
description: Build staff shift schedules as constraint problems — coverage demand, availability, rest gaps, fairness — with every constraint explicit and every violation reported instead of hidden in an unexplained roster.
metadata:
  source: skills/16-domain-specific/shift-scheduling.md
  category: 16-domain-specific
  version: "v1"
---

# Shift Scheduling

Category: Domain-Specific | Level: advanced | Stability: experimental | Version: v1

## Description

A roster is a set of assignments that satisfies stated constraints — or it is a wish. This skill treats scheduling as constraint programming: enumerate shifts and coverage requirements, encode hard constraints (availability, max hours, minimum rest between shifts) and soft ones (fairness in weekends and unpopular shifts), search for a feasible assignment, and report every constraint that could not be satisfied rather than quietly producing a broken roster.

## When to Use

Use for on-call rotations, support coverage, clinical or retail staffing — any recurring horizon where people must be assigned to shifts under rules.

Do not use for one-off task allocation with no recurring structure or constraints; that is task assignment, not scheduling.

## Inputs

| Input | Type | Required | Description |
|---|---|---|---|
| `staff` | `list[(person, availability)]` | Yes | People and the shifts they can work |
| `coverage_requirements` | `map[shift -> count]` | Yes | Minimum headcount per shift |
| `constraints` | `list[rule]` | Yes | Hard and soft rules with priorities |
| `horizon` | `list[day]` | Yes | The scheduling window |

## Procedure

1. Enumerate the shift grid across the horizon; every slot that needs coverage appears in the problem.
2. Encode hard constraints first — availability, maximum hours, minimum rest gaps; soft constraints carry explicit priorities.
3. Search for a feasible assignment; prefer solutions that minimize weighted soft-constraint violations.
4. When no feasible roster exists, report which constraints conflict and at which slots — do not silently drop coverage.
5. Compute fairness per person (shift counts, weekends, unpopular slots) and include it in the output.
6. On any later edit, revalidate the full roster; an edited roster is a new solution, not an exception to check.

## Outputs

| Output | Type | Description |
|---|---|---|
| `roster` | `map[shift -> list[person]]` | The assignment per slot |
| `violations` | `list[(constraint, slot)]` | Unsatisfied constraints, if any |
| `fairness` | `map[person -> summary]` | Per-person load and distribution metrics |

## Runnable Example

```python
def schedule(shifts, availability, coverage, max_shifts_per_person=2):
    """Greedy fill with a coverage check and explicit violation report."""
    roster, assigned, violations = {}, {}, []
    for shift in shifts:
        needed = coverage.get(shift, 0)
        candidates = [p for p in availability
                      if shift in availability[p] and assigned.get(p, 0) < max_shifts_per_person]
        chosen = candidates[:needed]
        roster[shift] = chosen
        for person in chosen:
            assigned[person] = assigned.get(person, 0) + 1
        if len(chosen) < needed:
            violations.append((shift, "coverage short"))
    return roster, violations

availability = {"ana": {"mon", "tue"}, "bo": {"mon"}, "cy": {"tue", "wed"}}
print(schedule(["mon", "tue", "wed"], availability, {"mon": 3, "tue": 1, "wed": 1}))
```

## Failure Modes

| Failure Mode | Cause | Mitigation |
|---|---|---|
| Hidden hard constraints | Rules applied verbally after publication | Encode every constraint before solving |
| Fairness ignored | One person absorbs the unpopular shifts | Track distribution and include it in the output |
| Missing rest gaps | Back-to-back night-then-day assignments | Encode minimum rest as a hard constraint |
| Unreported coverage gaps | Solver returns an incomplete roster silently | Emit violations with slots, always |
| Unvalidated edits | Manual fixes break constraints quietly | Revalidate the full roster after any edit |

## Security and Authority Boundary

A feasible schedule satisfies the stated constraints; labor-law compliance depends on those constraints being complete and current. Human approval of the published roster — and of constraint changes — remains mandatory.

## Evidence

This skill is grounded in dated public implementation references:

1. Wikipedia's overview of shift work (https://en.wikipedia.org/wiki/Shift_work).
2. Wikipedia's overview of the nurse scheduling problem (https://en.wikipedia.org/wiki/Nurse_scheduling_problem).

Honest boundary: these are implementation references, not adoption or demand evidence; this entry was added under the owner-directed corpus expansion recorded in `meta/memory/DECISIONS.md`, and no demand signal is claimed for it.

## Related Skills

- [Incident Response](incident-response.md) — on-call rosters that consume this scheduling discipline.
- [Alert Triage](alert-triage.md) — alert load data that informs coverage requirements.

## Changelog

| Date | Version | Change |
|---|---|---|
| `2026-10` | v1 | Initial entry added under the owner-directed corpus expansion |
