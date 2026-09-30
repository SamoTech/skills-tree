---
title: "Hypothesis Generation"
category: 02-reasoning
level: advanced
stability: stable
version: v2
description: "Generate multiple testable explanations for an observation, compare them using stated evidence, and identify discriminating checks."
added: "2025-03"
related: []
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-02-reasoning-hypothesis-generation.json)

# Hypothesis Generation

**Category:** `reasoning`  
**Skill Level:** `advanced`  
**Stability:** `stable`
**Added:** 2025-03

### Description

Propose testable explanations or predictions for observed phenomena based on available evidence.

### Example

```
Observation: API error rate spiked at 14:00.
Hypotheses:
  H1: Deployment at 13:58 introduced a regression.
  H2: Upstream provider had an outage.
  H3: Traffic surge exceeded rate limits.
Next: Check deploy logs and provider status page.
```

### Related Skills

- [Abductive Reasoning](abductive.md)
- [Causal Reasoning](causal.md)
- [Inductive Reasoning](inductive-reasoning.md)
- [Deductive Reasoning](deductive-reasoning.md)

## Failure Modes

- Unsupported assumptions: state assumptions explicitly and separate them from observed inputs.
- Ambiguous or incomplete premises: return uncertainty rather than fabricating missing constraints.
- Resource explosion: bound candidate counts, iterations, recursion, and external tool calls.

## Evidence

- https://agentskills.io/specification

Evidence status: implementation guidance only; no benchmark claim is made without reproducible evidence.
