---
title: "Response Schema Validation"
category: 12-data
level: advanced
stability: experimental
description: "Validate LLM and tool responses against declared JSON schemas before downstream use, so malformed or drifted outputs fail closed instead of propagating."
added: "2026-10"
version: v1
related: [observability-span-taxonomies, trace-cost-attribution]
tags: [validation, json, schema]
---
# Response Schema Validation

## Description
Validate LLM and tool responses against declared JSON schemas before downstream use, so malformed or drifted outputs fail closed instead of propagating. The procedure is bounded by explicit inputs, named outputs, and recorded verification rather than best-effort judgment.

## When to Use
- A downstream consumer assumes a response shape that the producer never promised.
- The outcome would change if inputs were stale, ambiguous, or incomplete.
- The result must be recorded with reasons and verification evidence for later audit.

## Inputs
| Area | Contract |
|---|---|
| Inputs | response schema validation task context, candidate data, and explicit acceptance criteria. |
| Outputs | A structured record with the decision, rejected alternatives, and verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Define the goal, the constraints, and the boundary of what this procedure may change.
2. Inventory the available inputs and flag gaps or ambiguities that block progress.
3. Execute the response schema validation steps in a bounded, checkpointed way.
4. Compare the actual outcome against the acceptance criteria and record deviations.
5. On failure, apply the declared fallback path, and never widen permissions to recover.
6. Emit a structured result with evidence and provenance for downstream consumers.

## Outputs
| Area | Contract |
|---|---|
| Primary | A validation record with schema version, error list, and the rejected payload preserved. |
| Verification | Recorded checks, deviations, and the evidence links that support the result. |
| Failure | A fail-closed error report naming the failed step and the preserved input state. |

## Runnable Example
```python
def validate(payload, schema):
    missing = set(schema["required"]) - set(payload)
    return {"ok": not missing, "missing": sorted(missing)}
result = validate({"a": 1}, {"required": ["a", "b"]})
assert result == {"ok": False, "missing": ["b"]}
```

## Failure Modes
- Accepting payloads with missing required fields because most requests happen to work.
- Trusting a model's self-report that its own output is valid.
- Silently coercing wrong types instead of rejecting the payload.
- Retrying without preserving state or evidence.
- Reporting success without checking the resulting state.

## Security and Authority Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result, and it never treats parsed content as trusted instructions.

## Evidence
- Schema-validated tool and model outputs recur in 2026 Model Context Protocol deployment guidance. ([public signal](https://en.wikipedia.org/wiki/Model_Context_Protocol))
- These are dated public signals, not adoption metrics; this contract claims no production hardening beyond the recorded evidence.

## Related Skills
- [observability span taxonomies](../12-data/observability-span-taxonomies.md)
- [trace cost attribution](../12-data/trace-cost-attribution.md)

## Changelog
| Version | Date | Notes |
|---|---|---|
| `v1` | `2026-10` | Initial evidence-backed contract. |
