---
title: "Consensus Voting"
category: 15-orchestration
level: advanced
stability: stable
version: v2
description: "Combine independent agent votes under an explicit voting rule, quorum, tie-break policy, and evidence boundary."
added: "2025-03"
related: [result-aggregation, debate-pattern]
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-15-orchestration-consensus-voting.json)

# Consensus Voting

**Category:** `orchestration`
**Skill Level:** `advanced`
**Stability:** `stable`
**Added:** 2025-03

### Description

Combine independent agent votes under an explicit voting rule, quorum, tie-break policy, and evidence boundary. The orchestration step is contract-first: validate state and inputs before acting, and verify the resulting state transition instead of trusting acknowledgements.

### Inputs / Outputs

| Direction | Field | Type | Contract |
|---|---|---|---|
| Input | votes | list of object | Per-agent votes with cited evidence and independence notes |
| Input | rule | object | Voting rule, quorum, and declared tie-break policy |
| Output | decision | object | The winning option with its tally and quorum status |
| Output | dissent | list of object | Non-winning votes kept visible with their evidence |

### Procedure
1. Declare the voting rule, quorum, and tie-break policy before collecting votes.
2. Verify voter independence; correlated voters count once or are flagged.
3. Collect votes with cited evidence, not bare preferences.
4. Tally under the declared rule; apply the tie-break exactly as declared.
5. Check the quorum; an unmet quorum produces no decision rather than a default win.
6. Publish the decision with the tally, the dissent, and the evidence boundary.

### Example

```python
votes = [{'voter': 'a', 'opt': 'x', 'evidence': ['log']}, {'voter': 'b', 'opt': 'x', 'evidence': []}, {'voter': 'c', 'opt': 'y', 'evidence': ['log']}]
rule = {'quorum': 3, 'tie_break': 'evidence_first'}
tally = {}
for v in votes: tally[v['opt']] = tally.get(v['opt'], 0) + 1
quorum_met = len(votes) >= rule['quorum']
top = max(tally, key=tally.get)
dissent = [v for v in votes if v['opt'] != top]
decision = {'opt': top if quorum_met else None, 'tally': tally}
assert decision['opt'] == 'x' and len(dissent) == 1
print({'decision': decision, 'dissent': [d['voter'] for d in dissent]})
```

### Related Skills

- [Debate Pattern](../09-agentic-patterns/debate-pattern.md) - adversarial reconciliation of claims
- [Result Aggregation](result-aggregation.md) - deterministic output combination
- [LLM Judge Calibration](../09-agentic-patterns/llm-judge-calibration.md) - calibrate adjudicating voters

## Failure Modes

- Correlated voters counted as independent evidence of correctness.
- Consensus treated as proof rather than a decision mechanism.
- Unmet quorum silently resolving to the default option.
- Dissent discarded instead of recorded with its evidence.

## Changelog
- v2 (2026-11): Structural modernization; added the input/output contract table, a skill-specific execution procedure, a deterministic example, and corpus-verified related links (replaced the unresolvable cross-category related references).
- v1 (2025-03): Initial entry.

## Evidence

- https://agentskills.io/specification

Evidence status: implementation guidance only; runtime behavior must be checked against the executing framework's documentation; no benchmark claim is made without reproducible evidence.
