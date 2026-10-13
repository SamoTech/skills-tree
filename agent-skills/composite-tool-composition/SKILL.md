---
name: composite-tool-composition
description: Compose composite tools from primitive ones with declared data flow, failure semantics, and per-step output validation.
metadata:
  source: skills/07-tool-use/composite-tool-composition.md
  category: 07-tool-use
  version: "v1"
---

# Composite Tool Composition

## Description
Compose composite tools from primitive ones with declared data flow, failure semantics, and per-step output validation. The procedure is constrained by explicit inputs and acceptance criteria rather than best-effort judgment alone.

## When to Use
- a workflow needs a composite tool built from existing primitives with clear failure semantics.
- Ambiguity or missing evidence would change the outcome.
- The result must be recorded with reasons and evidence for later verification.

## Inputs / Outputs
| Area | Contract |
|---|---|
| Inputs | Task context, candidate inputs, and explicit acceptance criteria for composite tool composition work. |
| Outputs | A decision or artifact with recorded reasons, rejected alternatives, and verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Define the goal, the constraints, and the boundary of what this procedure may change.
2. Inventory the available inputs and flag gaps or ambiguities that block progress.
3. Execute the composite tool composition steps in a bounded, checkpointed way.
4. Compare the actual outcome against the expected outcome and record deviations.
5. On failure, apply the declared fallback path, and never widen permissions to recover.
6. Emit a structured result with evidence and provenance for downstream consumers.

## Runnable Example
```python
def compose(steps, data):
    for name, fn in steps:
        data = fn(data)
        if data is None:
            raise ValueError("step failed: " + name)
    return data

steps = [("double", lambda d: d * 2), ("inc", lambda d: d + 1)]
assert compose(steps, 3) == 7
```

## Failure Modes
- Chaining steps without validating intermediate outputs.
- Swallowing a primitive failure as an empty result.
- No declared data contract between steps.
- Hiding cost by nesting composites inside composites.
- No per-step tracing when the chain fails midway.

## Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result.

## Evidence
Tool composition patterns are a recurring 2026 agent-framework request in public developer discussion; this is a dated signal, not an adoption metric.

## Related
- tool-schema-design.md
- tool-argument-construction.md
- function-calling.md
