---
title: "Progressive Skill Loading"
category: 03-memory
level: intermediate
stability: experimental
description: "Load skills into an agent context in escalating tiers - registry metadata first, the selected skill body second, and escalation only on measured need - so a large skill library costs a bounded, predictable token budget instead of loading every skill body up front."
added: "2026-10"
version: v1
related: ["03-memory", "context-compaction", "working-memory", "capability-based-skill-selection", "budget-management"]
---

# Progressive Skill Loading

Category: Memory | Level: intermediate | Stability: experimental | Version: v1

## Description

Progressive skill loading keeps the context cost of a skill library proportional to what the current task actually uses. Skills enter the context window in escalating tiers: cheap registry metadata is loaded first; the full body of a selected skill is loaded only when the task requires it; and loading additional skill bodies happens only when measured evidence shows the smaller tiers are insufficient.

This skill is intended for agent runtimes that consume large skill libraries. It does not replace retrieval, selection, or context compaction; it bounds the token cost of the skill layer itself.

## When to Use

Use when an agent consumes a library of many skills and the skill layer's token cost is large or unmeasured.

Do not use this to defer loading when the required skill is already known and affordable; load it directly.

## Inputs

| Input | Type | Required | Description |
|---|---|---|---|
| `skill_catalog` | `object` | Yes | Available skills with metadata-tier and full-body token costs |
| `token_budget` | `number` | Yes | Context budget reserved for the skill layer this turn |
| `task` | `object` | Yes | Current task and required capabilities |
| `selection` | `list` | No | Skills already selected by an upstream selection boundary |
| `load_policy` | `object` | No | Tier order, escalation thresholds, and load caps |

## Loading Procedure

1. Load the metadata tier for catalog skills within the reserved budget, cheapest first.
2. Record the measured token cost of the metadata tier against the reserved budget.
3. Resolve the required skill through the normal selection boundary.
4. Load the selected skill's full body and re-measure the remaining budget.
5. Escalate to loading additional skill bodies only when the loaded tiers demonstrably cannot satisfy the task.
6. Prefer unloading or compacting unused skill bodies over exceeding the budget.
7. Record which tiers were loaded, their measured cost, and every escalation decision.
8. Fail closed when the budget cannot cover even the required skill body; report instead of silently truncating.

## Outputs

| Output | Type | Description |
|---|---|---|
| `loaded_tiers` | `object` | Which skills are loaded at which tier and at what token cost |
| `tokens_used` | `number` | Measured skill-layer cost for the turn |
| `escalations` | `list` | Escalations performed, with the measured trigger |
| `unloaded` | `list` | Skills demoted or evicted from context |
| `status` | `string` | `OK`, `ESCALATED`, or `OVER-BUDGET` |

## Decision Contract

A valid loading decision must answer all of these questions:

- What is the measured token cost of the metadata tier?
- Which skill bodies are loaded, and why is each one loaded?
- What measured evidence triggered any escalation?
- What was evicted or compacted to stay within budget?
- What happens when the budget cannot cover the required body?

A skill must not be fully loaded merely because it might be relevant later.

## Runnable Example

```python
def progressive_load(catalog, budget, required_skill):
    """Load skills in tiers under a fixed token budget."""
    loaded = {}
    used = 0
    # Tier 1: metadata for every skill, cheapest first.
    for skill_id in sorted(catalog, key=lambda k: catalog[k]["metadata_cost"]):
        cost = catalog[skill_id]["metadata_cost"]
        if used + cost > budget:
            continue
        loaded[skill_id] = "metadata"
        used += cost
    # Tier 2: full body only for the required skill.
    body_cost = catalog[required_skill]["body_cost"] - catalog[required_skill]["metadata_cost"]
    if used + body_cost > budget:
        return {"loaded_tiers": loaded, "tokens_used": used, "status": "OVER-BUDGET"}
    loaded[required_skill] = "body"
    used += body_cost
    return {"loaded_tiers": loaded, "tokens_used": used, "status": "OK"}

catalog = {
    "context-compaction": {"metadata_cost": 40, "body_cost": 240},
    "working-memory": {"metadata_cost": 30, "body_cost": 180},
    "rag": {"metadata_cost": 35, "body_cost": 260},
}
result = progressive_load(catalog, budget=400, required_skill="rag")
print(result)
```

## Failure Modes

| Failure Mode | Cause | Mitigation |
|---|---|---|
| Silent full-load | Runtime loads every body at startup | Enforce tier order with measured costs |
| Budget overflow | Bodies loaded without re-measuring | Re-measure after every tier escalation |
| Starved metadata tier | Budget too small for even the metadata tier | Enlarge the budget or shrink the catalog; fail closed |
| Stale cost estimates | Token costs changed after skill edits | Re-measure costs on version change |
| Wrong-skill escalation | Body loaded on guessed relevance | Escalate only on selection-boundary decisions |
| Hidden truncation | Body cut mid-way without notice | Treat truncation as OVER-BUDGET, not OK |
| Cache incoherence | Loaded tier state diverges from the registry | Reload from the registry as source of truth |

## Security and Authority Boundary

Loading a skill body into context does not grant execution authority. A loaded skill still executes only within its declared permissions and the runtime's approval controls. Skill bodies from untrusted sources must pass the security audit boundary before being loaded at all.

## Evidence

This skill is motivated by dated public ecosystem evidence:

1. Public discussion of skill visibility in agent coding tools reports that carrying roughly 30-40 skills can consume on the order of 800-1,200 tokens per turn and requests explicit visibility tiers (https://github.com/anthropics/claude-code/issues/75376).
2. Microsoft Agent Framework documentation directs skills to stay under 5,000 tokens and describes progressive disclosure of skill content (https://learn.microsoft.com/en-us/agent-framework/agents/skills).
3. A 2026 agent-skills lifecycle survey describes token-budget-aware skill loading as a recurring lifecycle concern (https://redreamality.com/blog/agent-skills-2026-survey-lifecycle-map/).

Honest boundary: these signals establish that skill-layer token cost is a real, measured concern in agent runtimes; they are not adoption data, and the specific numbers are runtime-dependent examples, not universal constants.

The demand evidence is recorded in `meta/MOST-WANTED-SKILLS.md`.

## Related Skills

- [Context Compaction](context-compaction.md) — compacts conversation history; this skill bounds the skill layer before compaction is needed.
- [Working Memory](working-memory.md) — governs what the agent holds for the current task.
- [Capability-Based Skill Selection](../15-orchestration/capability-based-skill-selection.md) — decides which skill is needed; this skill decides how much of it to load.
- [Budget Management](../15-orchestration/budget-management.md) — enforces declared resource budgets; this skill applies that discipline to skill loading.

## Changelog

| Date | Version | Change |
|---|---|---|
| `2026-10` | v1 | Initial evidence-backed progressive skill-loading contract |
