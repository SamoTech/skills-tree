---
title: "Tool Schema Design"
category: 07-tool-use
level: intermediate
stability: experimental
description: "Design LLM tool schemas with disciplined names, bounded parameters, enumerated options, and structured errors so model calls stay valid, predictable, and cheap to validate."
added: "2026-10"
version: v1
related: ["function-calling", "tool-guardrails", "json-schema-validation"]
---

# Tool Schema Design

Category: Tool Use | Level: intermediate | Stability: experimental | Version: v1

## Description

A tool schema is the contract between a model and an execution surface, and most tool failures are schema failures: vague names, unbounded numbers, free text where an enum fits, and error shapes nobody planned. This skill defines the design contract: name tools after their effects, bound every parameter, prefer closed value sets, reject unknown keys, and return structured errors the caller can branch on.

## When to Use

Use when defining or revising an LLM-callable tool so that model errors become invalid calls instead of wrong effects.

Do not use for human-facing CLI design or internal library APIs; those audiences read documentation instead of schemas.

## Inputs

| Input | Type | Required | Description |
|---|---|---|---|
| `operations` | `list` | Yes | The distinct effects the surface must expose |
| `bounds` | `object` | Yes | Per-parameter limits including minimum and maximum |
| `enums` | `object` | No | Closed value sets per parameter |
| `error_catalog` | `list` | No | Structured error codes the surface can return |

## Procedure

1. Name each tool after the effect it performs, verb first; a schema named after its data invites misuse.
2. Give every parameter a type, a description, and where possible a bound; unbounded parameters are rejections in waiting.
3. Prefer closed enums over free text wherever the value space is known.
4. Mark required parameters explicitly and document what omitting an optional one means.
5. Reject unknown keys; permissive parsing lets hallucinated parameters reach execution.
6. Return errors as structured payloads with a stable code, a human-readable message, and a retryability flag.
7. Validate calls against the schema before execution; a call that fails validation never reaches the effect.
8. Version the schema; breaking changes take a new tool name, not a silent redefinition.

## Outputs

| Output | Type | Description |
|---|---|---|
| `schema` | `object` | The tool definition including parameter bounds and enums |
| `validation_errors` | `list` | Structured rejections naming the parameter and rule |
| `error_codes` | `list` | The stable error vocabulary callers branch on |
| `version` | `string` | The schema version callers pin against |

## Runnable Example

```python
TOOL_SCHEMA = {
    "name": "lookup_order",
    "description": "Fetch one order by its numeric identifier",
    "parameters": {
        "type": "object",
        "properties": {
            "order_id": {"type": "integer", "minimum": 1},
            "verbosity": {"type": "string", "enum": ["brief", "full"]},
        },
        "required": ["order_id"],
        "additionalProperties": False,
    },
}

def validate_call(schema, arguments):
    """Validate a tool call against the declared schema bounds."""
    errors = []
    for key in arguments:
        if key not in schema["parameters"]["properties"]:
            errors.append(f"unknown parameter: {key}")
    for key in schema["parameters"]["required"]:
        if key not in arguments:
            errors.append(f"missing required parameter: {key}")
    properties = schema["parameters"]["properties"]
    for key, value in arguments.items():
        spec = properties.get(key)
        if spec is None:
            continue
        minimum = spec.get("minimum")
        if minimum is not None and value < minimum:
            errors.append(f"{key} below minimum: {minimum}")
        if "enum" in spec and value not in spec["enum"]:
            errors.append(f"{key} not in allowed values: {spec['enum']}")
    return errors

print(validate_call(TOOL_SCHEMA, {"order_id": 0, "verbosity": "verbose", "extra": 1}))
```

## Failure Modes

| Failure Mode | Cause | Mitigation |
|---|---|---|
| Vague naming | A tool is named after its data instead of its effect | Name tools verb-first after what they do |
| Unbounded input | A numeric parameter has no limits | Declare minimum and maximum bounds |
| Enum omission | Free text sits where a closed set exists | Enumerate the value space |
| Permissive parsing | Unknown keys are silently ignored | Reject undeclared keys at validation |
| Shapeless errors | Errors come back as prose | Return a code, a message, and a retryability flag |

## Security and Authority Boundary

Designing a tool schema grants no execution authority. Schemas bound what a call may contain, not what it may do: the execution surface still enforces its own permission checks, rate limits, and audit logging. Error messages must never echo credentials or internal paths.

## Evidence

This skill is grounded in dated public implementation references:

1. The JSON Schema step-by-step getting-started guide (https://json-schema.org/learn/getting-started-step-by-step).
2. Python’s json module documentation (https://docs.python.org/3/library/json.html).

Honest boundary: these are implementation references, not adoption or demand evidence; this entry was added under the owner-directed corpus expansion recorded in `meta/memory/DECISIONS.md`, and no demand signal is claimed for it.

## Related Skills

- [Function Calling](function-calling.md) — executes declared functions; this skill defines the contract those calls are validated against.
- [Tool Guardrails](tool-guardrails.md) — bounds execution effects; this skill prevents invalid calls from reaching them.
- [JSON Schema Validation](../01-perception/json-schema-validation.md) — validates payload structure; this skill applies that discipline to LLM tool definitions.

## Changelog

| Date | Version | Change |
|---|---|---|
| `2026-10` | v1 | Initial entry added under the owner-directed corpus expansion |
