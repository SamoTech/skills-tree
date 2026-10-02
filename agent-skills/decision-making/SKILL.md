---
name: decision-making
description: Select among explicit options using stated goals, constraints, risks, evidence, and decision criteria; preserve trade-offs instead of hiding them.
metadata:
  source: skills/02-reasoning/decision-making.md
  category: 02-reasoning
  version: "v2"
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-02-reasoning-decision-making.json)

# Decision Making

**Category:** `reasoning`
**Skill Level:** `intermediate`
**Stability:** `stable`
**Added:** 2025-03

### Description

Select the best action from a set of options given context, constraints, and goals — using reasoning, scoring, or structured decision frameworks.

### Example

```
Options: [send_email, create_ticket, escalate_to_human]
Context: Customer reports critical production outage
Decision: escalate_to_human
Reason: Severity is critical and automated resolution confidence is low.
```

### Related Skills

- [Planning](planning.md)
- [Risk Assessment](risk-assessment.md)
- [Prioritization](prioritization.md)

## Failure Modes

- Unsupported assumptions: state assumptions explicitly and separate them from observed inputs.
- Ambiguous or incomplete premises: return uncertainty or request the missing constraint rather than fabricating one.
- Resource or search explosion: bound candidate counts, iterations, recursion, and external tool calls.

## Evidence

- https://agentskills.io/specification
- https://github.com/openai/openai-python

Evidence status: references support implementation guidance; no performance benchmark is claimed without reproducible benchmark evidence.

## Failure Modes

- Unsupported assumptions: state assumptions explicitly and separate them from observed inputs.
- Ambiguous or incomplete premises: return uncertainty rather than fabricating missing constraints.
- Resource explosion: bound candidate counts, iterations, recursion, and external tool calls.

## Evidence

- https://agentskills.io/specification

Evidence status: implementation guidance only; no benchmark claim is made without reproducible evidence.
