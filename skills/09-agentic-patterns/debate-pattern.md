---
title: "Debate Pattern"
category: 09-agentic-patterns
level: advanced
stability: stable
version: v2
description: "Use multiple role-separated agents to present, challenge, and reconcile competing claims under an explicit evidence protocol."
added: "2025-03"
related: [critic-agent, multi-agent-debate-resolution]
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-09-agentic-patterns-debate-pattern.json)

# Debate Pattern

**Category:** `agentic-patterns`
**Skill Level:** `advanced`
**Stability:** `stable`
**Added:** 2025-03

### Description

Use multiple role-separated agents to present, challenge, and reconcile competing claims under an explicit evidence protocol. Debate is an exposure mechanism, not a truth guarantee: agreement between agents counts as weak evidence and must be checked against sources.

### Inputs / Outputs

| Direction | Field | Type | Contract |
|---|---|---|---|
| Input | claim_or_question | text | The proposition or task the debate resolves |
| Input | roles | list of object | Assigned positions with an explicit evidence protocol |
| Output | positions | list of object | Each role's claim with its cited evidence |
| Output | synthesized_result | object | The reconciled claim, surviving objections, and open disagreements |

### Procedure
1. Assign roles and the evidence protocol (what counts as a citation) before any argument.
2. Have each role present its claim with cited evidence, not rhetoric.
3. Cross-examine: each role challenges the others' evidence, not their style.
4. Reconcile only claims that survive challenge; record disagreements that remain.
5. Verify the reconciled result against an independent source where stakes require it.
6. Report open disagreements and the evidence boundary instead of forcing consensus.

### Example

```python
positions = [
    {'role': 'pro', 'claim': 'cache hit', 'evidence': ['timing 12ms']},
    {'role': 'con', 'claim': 'cache miss', 'evidence': []},
]
protocol = {'min_evidence': 1}
surviving = [p['claim'] for p in positions if len(p['evidence']) >= protocol['min_evidence']]
result = {'resolved': surviving[0] if len(surviving) == 1 else None,
          'open': [p['role'] for p in positions if len(p['evidence']) < protocol['min_evidence']]}
assert result['resolved'] == 'cache hit' and result['open'] == ['con']
print(result)
```

### Related Skills

- [Critic Agent](critic-agent.md) - single-role critique against a rubric
- [Multi-Agent Debate Resolution](multi-agent-debate-resolution.md) - resolve competing agent claims
- [LLM Judge Calibration](llm-judge-calibration.md) - calibrate the adjudicator
- [Output Guardrails](../14-security/output-guardrails.md) - validate the synthesized result

## Failure Modes

- Treating agent agreement as proof; correlated models agree on shared errors.
- Letting rhetorical strength substitute for cited evidence.
- Forcing consensus and burying open disagreements.
- Running debates without a declared evidence protocol.

## Changelog
- v2 (2026-11): Structural modernization; added the input/output contract table, a skill-specific execution procedure, a deterministic example, and corpus-verified related links (replaced the unresolvable cross-category related references).
- v1 (2025-03): Initial entry.

## Evidence

- https://agentskills.io/specification

Evidence status: implementation guidance only; pattern behavior must be checked against current framework documentation; no benchmark claim is made without reproducible evidence.
