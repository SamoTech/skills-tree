---
name: calculator
description: Perform deterministic calculations with explicit inputs, units, assumptions, and verifiable outputs.
metadata:
  source: skills/07-tool-use/calculator.md
  category: 07-tool-use
  version: "v2"
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-07-tool-use-calculator.json)

# Calculator

**Category:** `tool-use`
**Skill Level:** `advanced`
**Stability:** `stable`
**Added:** 2026-09

### Description

Perform deterministic calculations with explicit inputs, units, assumptions, and verifiable outputs. The invocation is contract-first: validate the tool interface and inputs before calling, and verify the observable outcome afterwards rather than trusting acknowledgements.

### Inputs / Outputs

| Direction | Field | Type | Contract |
|---|---|---|---|
| Input | expression | object | The operation with explicit operands, units, and precision |
| Input | assumptions | list of string | Rounding, unit, and model assumptions stated before computing |
| Output | result | object | The computed value with units and precision |
| Output | check | object | An independent sanity check (inverse operation, order-of-magnitude, or bound) |

### Procedure
1. State the inputs with units and the required output precision before computing.
2. Record the assumptions (rounding, unit conversion, model) that the result depends on.
3. Compute with the deterministic tool; avoid re-deriving arithmetic mentally.
4. Validate the result with an independent check: inverse operation, bound, or order-of-magnitude.
5. Report the result with units, precision, and the assumptions that bound its validity.

### Example

```python
km, hours = 420.0, 5.0
speed_kmh = km / hours
assert abs(speed_kmh - 84.0) < 1e-9
assert round(km / speed_kmh, 6) == hours
print(f'{speed_kmh} km/h; inverse check passes')
```

### Related Skills

- [Tool Argument Construction](tool-argument-construction.md) - build well-formed tool inputs
- [Tool Output Validation](tool-output-validation.md) - verify computed results

## Failure Modes

- Mixing units or dropping them from the result.
- Reporting precision the method does not support.
- Skipping the independent sanity check.
- Presenting a rounded estimate as exact.

## Changelog
- v2 (2026-11): Structural modernization; added the input/output contract table, a deterministic example, an execution procedure, and corpus-verified related links (replaced the non-corpus input-guardrails/AI_CONSTITUTION.md pointers where present).
- v1 (2026-09): Initial entry.

## Evidence

- https://agentskills.io/specification

Evidence status: implementation guidance only; provider behavior must be checked against current provider documentation; no benchmark claim is made without reproducible evidence.
