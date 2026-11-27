---
name: budget-management
description: Track and enforce declared resource budgets across an agent workflow, including token, time, tool, or monetary limits.
metadata:
  source: skills/15-orchestration/budget-management.md
  category: 15-orchestration
  version: "v2"
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-15-orchestration-budget-management.json)

# Budget Management

**Category:** `orchestration`
**Skill Level:** `advanced`
**Stability:** `stable`
**Added:** 2025-03

### Description

Track and enforce declared resource budgets across an agent workflow, including token, time, tool, or monetary limits. The orchestration step is contract-first: validate state and inputs before acting, and verify the resulting state transition instead of trusting acknowledgements.

### Inputs / Outputs

| Direction | Field | Type | Contract |
|---|---|---|---|
| Input | budget | object | Declared ceilings per resource (tokens, time, calls, currency) |
| Input | ledger | list of object | Consumption records per step with their costs |
| Output | remaining | object | Remaining budget per resource against the ceilings |
| Output | action | enum | continue, degrade, or halt, with the binding constraint named |

### Procedure
1. Declare the ceilings per resource before the workflow starts; estimates are separate from ceilings.
2. Record consumption per step with its cost and the step identifier.
3. Compare the running ledger against the ceilings before each expensive step.
4. Enforce hard ceilings where the runtime supports them; surface estimates as estimates.
5. Degrade or halt when a ceiling is reached, naming the binding constraint.
6. Report final consumption with the ledger so the budget decision is auditable.

### Example

```python
budget = {'tokens': 10000, 'tool_calls': 20}
ledger = [{'step': 'plan', 'tokens': 3200, 'calls': 2}, {'step': 'search', 'tokens': 4100, 'calls': 9}]
used = {r: sum(e.get('tokens' if r == 'tokens' else 'calls', 0) for e in ledger) for r in budget}
remaining = {r: budget[r] - used[r] for r in budget}
action = 'continue' if all(v > 2000 for v in remaining.values()) else 'degrade'
assert used['tokens'] == 7300 and remaining['tool_calls'] == 9 and action == 'continue'
print({'remaining': remaining, 'action': action})
```

### Related Skills

- [Workflow Cost Ceiling](workflow-cost-ceiling.md) - workflow-level spending bounds
- [Cost-Aware Model Routing](cost-aware-model-routing.md) - route steps to affordable models
- [Least Privilege Scoping](../14-security/least-privilege-scoping.md) - bound what paid calls may access

## Failure Modes

- Estimates treated as ceilings, so consumption silently overshoots.
- No per-step ledger, making the budget decision unauditable.
- Continuing past a hard ceiling because an estimate looked safe.
- Halting without naming the binding constraint or the recovery path.

## Changelog
- v2 (2026-11): Structural modernization; added the input/output contract table, a skill-specific execution procedure, a deterministic example, and corpus-verified related links (replaced the unresolvable cross-category related references).
- v1 (2025-03): Initial entry.

## Evidence

- https://agentskills.io/specification

Evidence status: implementation guidance only; runtime behavior must be checked against the executing framework's documentation; no benchmark claim is made without reproducible evidence.
