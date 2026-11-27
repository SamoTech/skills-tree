---
name: constitutional-ai
description: Apply a declared set of principles to critique and revise generated outputs without treating those principles as universal law.
metadata:
  source: skills/09-agentic-patterns/constitutional-ai.md
  category: 09-agentic-patterns
  version: "v2"
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-09-agentic-patterns-constitutional-ai.json)

# Constitutional AI

**Category:** `agentic-patterns`
**Skill Level:** `advanced`
**Stability:** `stable`
**Added:** 2025-03

### Description

Apply a declared, versioned set of principles to critique and revise generated outputs. Principles are policy for this workflow only, never universal law: conflicts between principles, and principles that cannot be applied mechanically, are recorded rather than silently resolved.

### Inputs / Outputs

| Direction | Field | Type | Contract |
|---|---|---|---|
| Input | draft | text | The output to critique and revise |
| Input | principles | list of object | Versioned, scoped principles with an explicit revision |
| Output | revised_output | text | The revised draft with change notes tied to principle ids |
| Output | conflicts | list of object | Unresolved principle conflicts left for human decision |

### Procedure
1. Fix the principle set and its version before critiquing; never invent principles mid-review.
2. Evaluate the draft against each principle separately and cite the passage that triggers a violation.
3. Revise the draft to satisfy the principles, keeping a change note per revision.
4. Record any principle pair that conflicts, or any principle that cannot be applied mechanically, as an open conflict.
5. Verify the revision against the declared principle version before acceptance.
6. Report conflicts and residual uncertainty instead of silently resolving them.

### Example

```python
draft = {'claims': ['Tool ran', 'Run took 3.2s'], 'unverified': [False, True]}
principles = {'v3': {'cite_sources': True, 'flag_unverified': True}}
violations = [c for c, ok in zip(draft['claims'], draft['unverified'])
              if not ok and principles['v3']['flag_unverified']]
revised = {'text': draft['claims'], 'flags': ['unverified: run took 3.2s'],
           'principles_version': 'v3', 'conflicts': []}
assert violations == [] and revised['principles_version'] == 'v3'
print(revised['flags'])
```

### Related Skills

- [Critic Agent](critic-agent.md) - role-separated critique against explicit criteria
- [Reflection](reflection.md) - critique-and-revision pass before acceptance
- [Input Guardrails](../14-security/input-guardrails.md) - bound what enters the critique loop
- [Output Guardrails](../14-security/output-guardrails.md) - validate the revised output

## Failure Modes

- Treating workflow principles as universal law or as the host agent's security policy.
- Revising against an undeclared or mid-review-changed principle version.
- Silently resolving conflicting principles instead of recording them.
- Claiming the revision is verified without re-checking it against the declared criteria.

## Changelog
- v2 (2026-11): Structural modernization; added the input/output contract table, a skill-specific execution procedure, a deterministic example, and corpus-verified related links (replaced the unresolvable cross-category related references).
- v1 (2025-03): Initial entry.

## Evidence

- https://agentskills.io/specification

Evidence status: implementation guidance only; pattern behavior must be checked against current framework documentation; no benchmark claim is made without reproducible evidence.
