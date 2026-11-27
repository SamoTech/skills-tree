---
title: "Critic Agent"
category: 09-agentic-patterns
level: advanced
stability: stable
version: v2
description: "Use a separate critic role to inspect an agent output against explicit criteria and return actionable findings for revision or acceptance."
added: "2025-03"
related: [reflection, self-refine-critique-loop]
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-09-agentic-patterns-critic-agent.json)

# Critic Agent

**Category:** `agentic-patterns`
**Skill Level:** `advanced`
**Stability:** `stable`
**Added:** 2025-03

### Description

Use a separate critic role to inspect an agent output against explicit criteria and return actionable findings. The critic is contract-first: it scores against a declared rubric, cites the evidence for each finding, and never converts subjective scores into objective truth.

### Inputs / Outputs

| Direction | Field | Type | Contract |
|---|---|---|---|
| Input | candidate_output | text | The generated output under review |
| Input | rubric | list of object | Declared criteria, each with a check the critic can actually perform |
| Output | critique | list of object | Findings with criterion id, verdict, cited reason, and severity |
| Output | verdict | enum | accept, revise, or reject, with the decisive findings named |

### Procedure
1. Fix the rubric and its version before reviewing; the critic never scores against undeclared criteria.
2. Check each criterion independently and cite the exact passage supporting the verdict.
3. Separate subjective preference from checkable defects; label which is which.
4. Return findings as actionable revisions, not as an unexplained score.
5. Verify the critic's findings against the output before acting on them; a critic can reproduce generator errors.
6. Accept, revise, or reject with the decisive findings named in the record.

### Example

```python
output = {'answer': '42 rows', 'cites': ['query log'], 'states_limit': True}
rubric = {'v2': {'grounded': output['cites'] != [], 'bounded': output['states_limit']}}
findings = [{'criterion': k, 'verdict': 'pass' if v else 'fail'}
            for k, v in rubric['v2'].items()]
verdict = 'accept' if all(f['verdict'] == 'pass' for f in findings) else 'revise'
assert findings == [{'criterion': 'grounded', 'verdict': 'pass'},
                    {'criterion': 'bounded', 'verdict': 'pass'}]
print(verdict)
```

### Related Skills

- [Reflection](reflection.md) - critique-and-revision pass inside one agent
- [Self-Refine Critique Loop](self-refine-critique-loop.md) - iterate critique until the rubric passes
- [LLM Judge Calibration](llm-judge-calibration.md) - calibrate subjective scoring
- [Input Guardrails](../14-security/input-guardrails.md) - bound the critic's inputs

## Failure Modes

- The critic reproduces the generator's errors and confirms a wrong answer.
- Subjective scores presented as objective truth without cited reasons.
- Scoring against criteria that were never declared in the rubric.
- Acting on critique without verifying the findings against the output.

## Changelog
- v2 (2026-11): Structural modernization; added the input/output contract table, a skill-specific execution procedure, a deterministic example, and corpus-verified related links (replaced the unresolvable cross-category related references).
- v1 (2025-03): Initial entry.

## Evidence

- https://agentskills.io/specification

Evidence status: implementation guidance only; pattern behavior must be checked against current framework documentation; no benchmark claim is made without reproducible evidence.
