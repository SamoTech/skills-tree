---
name: ethical-reasoning
description: Analyze decisions across explicit ethical frameworks and stakeholder impacts without presenting a framework-dependent judgment as objective fact.
metadata:
  source: skills/02-reasoning/ethical-reasoning.md
  category: 02-reasoning
  version: "v3"
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-02-reasoning-ethical-reasoning.json)

# Ethical Reasoning

Category: reasoning | Level: advanced | Stability: stable

## Description
Evaluate actions and decisions against explicit ethical frameworks (utilitarian, deontological, virtue ethics) and stakeholder impacts, presenting framework-dependent conclusions as such rather than as objective fact.

## When to Use
- Policy or product decisions with foreseeable effects on people who cannot veto them
- Reviewing automated decision systems for differential impact on affected groups
- Preparing escalations where a human must own an ethically loaded choice

## Inputs / Outputs

| Direction | Field | Type | Contract |
|---|---|---|---|
| Input | `action` | string | The decision or action under evaluation |
| Input | `stakeholders` | list of string | Affected parties, including those without a voice in the decision |
| Input | `frameworks` | optional list of string | Frameworks to apply; defaults to utilitarian, deontological, virtue |
| Output | `analysis` | per-framework findings | What each framework says, kept separate per framework |
| Output | `disagreements` | list of string | Where frameworks conflict; these are the human-decision points |
| Output | `affected` | per-stakeholder impact | Concrete impact per stakeholder group with its evidence |

## Example
```python
def stakeholder_matrix(impacts: dict[str, dict[str, str]]) -> None:
    """Print a per-stakeholder impact table; 'unknown' must stay explicit."""
    for group, effects in impacts.items():
        for dimension, effect in effects.items():
            print(f"{group:24} {dimension:12} {effect}")

stakeholder_matrix({
    "patients": {"cost": "-20% billing overhead", "privacy": "records shared with vendor"},
    "admin_staff": {"employment": "15% of roles eliminated"},
    "hospital": {"budget": "cost reduction", "liability": "vendor contract required"},
})
```

## Procedure
1. Name the action precisely and identify every affected stakeholder group, including unrepresented ones.
2. Apply each framework separately and record its conclusion without blending them.
3. Mark where frameworks disagree; those conflicts are decisions for accountable humans, not model output.
4. Assess distribution: who gains, who bears the cost, and whether consent was possible.
5. Surface the least-defensible aspect of the favored option before recommending anything.
6. Escalate with the structured analysis when the decision is irreversible or affects unconsenting parties.

## Failure Modes
- Framework selection bias: apply the named frameworks separately and report disagreement instead of cherry-picking a verdict.
- Missing affected stakeholder groups: enumerate stakeholders from the action's causal footprint, not from who is in the room.
- Presenting a framework-dependent judgment as objective fact: label every conclusion with the framework that produced it.
- Abstraction that hides concrete harm: keep impacts concrete (who, what, when) rather than utilitarian aggregates.
- Moral rubber-stamping: if the analysis cannot name anything a reasonable person might object to, redo it.

## Related
- [Decision Making](decision-making.md)
- [Causal Reasoning](causal.md)

## Changelog
- v3 (2026-11): Structural modernization; merged the three duplicated failure-mode and evidence sections into one authoritative set, added the input/output contract table, procedure, and stakeholder-matrix example.
- v1 (2026-04): Initial entry.

## Evidence

- https://agentskills.io/specification

Evidence status: implementation guidance only; no benchmark claim is made without reproducible evidence.
