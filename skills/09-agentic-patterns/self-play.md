---
title: "Self-Play"
category: 09-agentic-patterns
level: advanced
stability: stable
version: v2
description: "Train or improve an agent through controlled adversarial interaction between role-separated policies or prompts."
added: "2025-03"
related: [debate-pattern, exploration-exploitation-balancing]
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-09-agentic-patterns-self-play.json)

# Self-Play

**Category:** `agentic-patterns`
**Skill Level:** `advanced`
**Stability:** `stable`
**Added:** 2025-03

### Description

Train or improve an agent through controlled adversarial interaction between role-separated policies or prompts. Improvement is measured on a held-out evaluation against the real task objective, never on the self-play reward alone, which can be gamed.

### Inputs / Outputs

| Direction | Field | Type | Contract |
|---|---|---|---|
| Input | policy_or_prompt | object | The improving policy with its version |
| Input | opponent_policy | object | The role-separated adversary with its version |
| Output | evaluation_metric | object | Held-out metric against the real task objective |
| Output | caveats | list of string | Proxy risks, collapse signs, and evaluator weaknesses observed |

### Procedure
1. Separate the improving and opponent roles with distinct versions and prompts.
2. Run controlled interactions and record the outcomes per episode.
3. Measure improvement on a held-out evaluation tied to the real task objective.
4. Watch for proxy optimization, strategy collapse, and evaluator exploits; record them as caveats.
5. Gate acceptance on the held-out metric, never on the self-play reward.
6. Report both metric versions (policy and opponent) so the comparison is reproducible.

### Example

```python
policy, opponent = 'p-v3', 'o-v3'
episodes = [{'winner': policy}, {'winner': opponent}, {'winner': policy}]
heldout = {'p-v3': 0.62, 'p-v2': 0.55}   # real-task metric, held-out set
gate = 0.60
accepted = heldout[policy] >= gate
wins = sum(1 for e in episodes if e['winner'] == policy) / len(episodes)
assert accepted and wins == 2 / 3
caveats = ['proxy: self-play reward up but held-out gain is 0.07']
print({'heldout': heldout[policy], 'gate': gate, 'accepted': accepted, 'caveats': caveats})
```

### Related Skills

- [Debate Pattern](debate-pattern.md) - adversarial structure for claims rather than policies
- [Exploration-Exploitation Balancing](exploration-exploitation-balancing.md) - pacing the adversarial search
- [Reward Hacking Detection](reward-hacking-detection.md) - catch proxy gaming
- [Agent Eval Harness Design](agent-eval-harness-design.md) - the held-out evaluation contract

## Failure Modes

- Optimizing the self-play reward while the held-out task metric stagnates.
- Strategy collapse into repetitive interactions without new signal.
- Exploiting a weakness in the evaluator instead of improving the task behavior.
- Accepting improvements measured only on the self-play reward.

## Changelog
- v2 (2026-11): Structural modernization; added the input/output contract table, a skill-specific execution procedure, a deterministic example, and corpus-verified related links (replaced the unresolvable cross-category related references).
- v1 (2025-03): Initial entry.

## Evidence

- https://agentskills.io/specification

Evidence status: implementation guidance only; pattern behavior must be checked against current framework documentation; no benchmark claim is made without reproducible evidence.
