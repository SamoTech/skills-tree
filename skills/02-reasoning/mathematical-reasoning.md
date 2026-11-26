---
title: "Mathematical Reasoning"
category: 02-reasoning
level: intermediate
stability: stable
version: v3
description: "Solve bounded mathematical problems with explicit assumptions, equations, units, intermediate checks, and a verifiable final result."
added: "2025-03"
related: []
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-02-reasoning-mathematical-reasoning.json)

# Mathematical Reasoning

**Category:** `reasoning`
**Skill Level:** `intermediate`
**Stability:** `stable`
**Added:** 2025-03

### Description

Solve mathematical problems step by step (arithmetic, algebra, calculus, statistics, and logic) with explicit assumptions, units, intermediate checks, and a verifiable final result.

### Inputs / Outputs

| Direction | Field | Type | Contract |
|---|---|---|---|
| Input | `problem` | string | The problem statement with all given quantities and units |
| Input | `assumptions` | optional list of string | Simplifying assumptions; anything unstated must be listed here |
| Input | `precision` | optional number | Required precision of the final result |
| Output | `result` | string or number | The final answer with correct units |
| Output | `steps` | list of string | Equation-level steps, each independently checkable |
| Output | `checks` | list of string | Verification passes (unit check, magnitude check, substitution) |

### Procedure
1. Restate the problem with every given quantity, unit, and unknown made explicit.
2. List the assumptions required to solve it; do not leave them implicit.
3. Derive the solution in equation-level steps, keeping units in every step.
4. Verify the result by substitution, a second method, or a magnitude sanity check.
5. Round only at the end, to the requested precision.
6. Report the result with its units, assumptions, and verification evidence.

### Example

```python
# pip install sympy
import sympy

def train_speed_kmh_to_ms(distance_km: float, hours: float) -> dict:
    kmh = distance_km / hours
    ms = kmh * 1000 / 3600
    x = sympy.symbols("x")
    check = sympy.solve(sympy.Eq(x * 3600 / 1000, distance_km / hours), x)
    return {"kmh": kmh, "ms": round(ms, 2), "unit_check_ms": float(check[0])}

print(train_speed_kmh_to_ms(120, 1.5))
```

### Frameworks

- Chain of Thought prompting
- Wolfram Alpha tool
- Python `sympy`, `math` via code execution
- OpenAI o3 / o4-mini (native math reasoning)

### Related Skills

- [Chain of Thought](chain-of-thought.md)
- [Calculator](../07-tool-use/calculator.md)

## Failure Modes

- Unsupported assumptions: state assumptions explicitly and separate them from observed inputs.
- Ambiguous or incomplete premises: return uncertainty rather than fabricating missing constraints.
- Unit errors: carry units through every step and verify the final unit algebraically.
- Unverified arithmetic: check the result by substitution or a second method before reporting it.
- Resource explosion: bound candidate counts, iterations, recursion, and external tool calls.

## Changelog
- v3 (2026-11): Structural modernization; added the input/output contract table, procedure, and a deterministic verification example.
- v1 (2025-03): Initial entry.

## Evidence

- https://agentskills.io/specification

Evidence status: implementation guidance only; no benchmark claim is made without reproducible evidence.
