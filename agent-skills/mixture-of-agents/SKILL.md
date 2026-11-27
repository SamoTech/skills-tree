---
name: mixture-of-agents
description: Route a task through multiple specialized agents and aggregate their outputs using an explicit synthesis policy.
metadata:
  source: skills/09-agentic-patterns/mixture-of-agents.md
  category: 09-agentic-patterns
  version: "v2"
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-09-agentic-patterns-mixture-of-agents.json)

# Mixture of Agents

**Category:** `agentic-patterns`
**Skill Level:** `advanced`
**Stability:** `stable`
**Added:** 2025-03

### Description

Route a task through multiple specialized agents and aggregate their outputs using an explicit synthesis policy declared before execution. The policy states how disagreements are resolved and what counts as a veto, so aggregation is reproducible rather than improvised.

### Inputs / Outputs

| Direction | Field | Type | Contract |
|---|---|---|---|
| Input | task | text | The task routed to the specialist agents |
| Input | agent_outputs | list of object | Per-agent answers with their self-reported confidence and evidence |
| Output | synthesized_output | object | The aggregated answer under the declared synthesis policy |
| Output | dissent | list of object | Agent answers the policy overruled, kept visible |

### Procedure
1. Declare the synthesis policy (precedence, majority, or adjudicator) and any veto rule before routing.
2. Route the task to the specialists with the same task statement and evidence boundary.
3. Collect outputs with each agent's cited evidence and confidence.
4. Aggregate strictly under the declared policy; record overruled answers as dissent.
5. Measure whether added agents provide incremental signal before scaling the mixture.
6. Report the synthesized output with the dissent list and the policy version used.

### Example

```python
policy = {'v1': 'majority_then_precedence'}
outputs = [
    {'agent': 'retriever', 'answer': '2024-03', 'evidence': ['doc 7']},
    {'agent': 'analyst', 'answer': '2024-03', 'evidence': []},
    {'agent': 'verifier', 'answer': '2025-01', 'evidence': ['ledger']},
]
votes = {}
for o in outputs: votes[o['answer']] = votes.get(o['answer'], 0) + 1
top = max(votes, key=votes.get)
dissent = [o for o in outputs if o['answer'] != top]
assert top == '2024-03' and len(dissent) == 1
print({'answer': top, 'policy': policy['v1'], 'dissent': [d['agent'] for d in dissent]})
```

### Related Skills

- [Debate Pattern](debate-pattern.md) - adversarial reconciliation of competing claims
- [Critic Agent](critic-agent.md) - rubric-based review of a candidate answer
- [Input Guardrails](../14-security/input-guardrails.md) - bound what enters each agent
- [Output Guardrails](../14-security/output-guardrails.md) - validate the aggregated result

## Failure Modes

- Scaling the mixture without measuring incremental signal, only cost.
- Aggregating under an undeclared or post-hoc policy.
- Hiding overruled agent answers instead of recording dissent.
- Correlated agent errors counted as independent votes.

## Changelog
- v2 (2026-11): Structural modernization; added the input/output contract table, a skill-specific execution procedure, a deterministic example, and corpus-verified related links (replaced the unresolvable cross-category related references).
- v1 (2025-03): Initial entry.

## Evidence

- https://agentskills.io/specification

Evidence status: implementation guidance only; pattern behavior must be checked against current framework documentation; no benchmark claim is made without reproducible evidence.
