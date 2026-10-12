---
name: curriculum-sequencing
description: Order learning units into a dependency-respecting path — prerequisites as edges, cycle detection, mastery gates — so study plans stay coherent, individually paced, and free of impossible orders.
metadata:
  source: skills/16-domain-specific/curriculum-sequencing.md
  category: 16-domain-specific
  version: "v1"
---

# Curriculum Sequencing

Category: Domain-Specific | Level: intermediate | Stability: experimental | Version: v1

## Description

A curriculum is a directed graph wearing a reading list's clothes. Sequencing it means extracting prerequisite edges from stated dependencies, verifying the graph is acyclic, ordering units topologically, and placing mastery gates between a unit and everything that depends on it. Placement tests adjust the entry point by skipping proven material — not by deleting it, since a skipped unit must remain visible in the path's record.

## When to Use

Use when a set of lessons, modules, or skills must be ordered for a learner — course assembly, onboarding plans, or personalized study paths.

Do not use for a flat list with no real dependencies; sorting adds ceremony without value when the graph has no edges.

## Inputs

| Input | Type | Required | Description |
|---|---|---|---|
| `units` | `list[unit_id]` | Yes | All learning units in scope |
| `prerequisites` | `list[(before, after)]` | Yes | Stated edges: unit before unit |
| `learner_profile` | `map[unit -> mastered]` | Yes | Placement results per learner |

## Procedure

1. Extract prerequisite edges exactly as stated; an assumed-but-unstated dependency is an edge nobody can audit.
2. Detect cycles first; a cyclic curriculum has no valid order, only a hidden wrong edge to fix.
3. Produce a topological order of the units; ties break deterministically (by unit id) for reproducible plans.
4. Apply placement: units already mastered are marked skipped-in-place, never removed from the record.
5. Insert mastery gates before dependents: a unit's dependents unlock only when its gate is passed.
6. Emit the path with per-unit status (assigned, skipped, gated) and the edge set it was derived from.

## Outputs

| Output | Type | Description |
|---|---|---|
| `path` | `list[unit_id]` | The dependency-respecting order |
| `cycle_error` | `cycle | null` | The offending units, if the graph is cyclic |
| `gates` | `list[unit_id]` | Units whose mastery gates downstream dependents |

## Runnable Example

```python
def sequence(units, edges, mastered=()):
    """Topologically order units or report the blocking cycle."""
    remaining = {u for u in units if u not in mastered}
    incoming = {u: set() for u in units}
    for before, after in edges:
        if after in incoming:
            incoming[after].add(before)
    order = []
    ready = sorted(u for u in remaining if not (incoming[u] & remaining))
    while ready:
        unit = ready.pop(0)
        order.append(unit)
        remaining.discard(unit)
        ready = sorted(u for u in remaining if not (incoming[u] & remaining))
    if remaining:
        return None, sorted(remaining)
    return order, None

edges = [("algebra", "calculus"), ("calculus", "physics")]
print(sequence(["physics", "calculus", "algebra"], edges))
print(sequence(["a", "b"], [("a", "b"), ("b", "a")]))
```

## Failure Modes

| Failure Mode | Cause | Mitigation |
|---|---|---|
| Circular prerequisites | Units that depend on each other transitively | Detect cycles before ordering; fix the graph |
| Hidden prerequisites | Assumed knowledge not stated as edges | Make every dependency an explicit, auditable edge |
| Ungated advancement | Dependents reached before mastery | Insert mastery gates before dependents |
| Placement amnesia | Skipped units vanish from records | Mark skipped-in-place; keep the full path visible |
| Orphan units | Units no path can reach | Surface unreachable units for graph repair |

## Security and Authority Boundary

Sequencing orders material; it certifies nothing about mastery. What a completed path means is decided by assessment quality, which this skill consumes but does not provide.

## Evidence

This skill is grounded in dated public implementation references:

1. Wikipedia's overview of topological sorting (https://en.wikipedia.org/wiki/Topological_sorting).
2. Wikipedia's overview of curriculum as a structured program of learning (https://en.wikipedia.org/wiki/Curriculum).

Honest boundary: these are implementation references, not adoption or demand evidence; this entry was added under the owner-directed corpus expansion recorded in `meta/memory/DECISIONS.md`, and no demand signal is claimed for it.

## Related Skills

- [Lesson Plan](lesson-plan.md) — the per-unit content a sequence orders.
- [Flashcard Creation](flashcard-creation.md) — spaced repetition material attached to sequenced units.

## Changelog

| Date | Version | Change |
|---|---|---|
| `2026-10` | v1 | Initial entry added under the owner-directed corpus expansion |
