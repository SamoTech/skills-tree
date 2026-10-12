---
name: tool-output-validation
description: Check tool outputs against a declared schema before they enter the reasoning stream, so a malformed result fails loudly at the boundary instead of downstream.
metadata:
  source: skills/07-tool-use/tool-output-validation.md
  category: 07-tool-use
  version: "v1"
---

# Tool Output Validation

Category: Tool Use | Level: intermediate | Stability: experimental | Version: v1

## Description

A tool result is untrusted input with a confident tone: it arrives as a string, a dict, or a truncated fragment, and whatever shape it claims is a claim. This skill moves the checking to the boundary: each expected output is declared as a schema, each result is validated on arrival, and a failure is reported as a structured error with the offending path — not smuggled into the conversation for the caller to misread. Validation failures are normal control flow, not exceptions to silence.

## When to Use

Use whenever a tool result feeds decisions — structured data, numeric values, identifiers — and especially when results come from external services outside your control.

Do not validate ad hoc fields nobody consumes; a schema that checks everything protects nothing in particular and costs every call.

## Inputs

| Input | Type | Required | Description |
|---|---|---|---|
| `tool_result` | `any` | Yes | The raw output returned by the tool |
| `schema` | `schema` | Yes | The declared shape the result must satisfy |
| `on_error` | `enum` | No | Reject, repair, or re-request when validation fails |

## Procedure

1. Declare the schema for what the result must contain — required fields, types, and bounds — before calling the tool.
2. Validate on arrival: check presence first, then types, then value constraints such as ranges or enum membership.
3. Collect every violation with its path rather than failing on the first, so one pass describes the whole gap.
4. Route failures by policy: reject the result, attempt a bounded repair, or re-request once with a corrected call.
5. Never stringify a failed result into the reasoning stream; a rejected result enters as an error record with its path and reason.
6. Keep the schema under version control beside the tool integration, and bump it when the upstream contract changes.

## Outputs

| Output | Type | Description |
|---|---|---|
| `validated` | `any` | The checked result, ready for downstream reasoning |
| `violations` | `list` | Per-path failures with type, constraint, and observed value |

## Runnable Example

```python
def validate(record, schema):
    violations = []
    for field, spec in schema.items():
        if field not in record:
            violations.append({"path": field, "error": "missing"})
            continue
        observed = record[field]
        expected = spec["type"]
        if expected is not type(observed):
            name = type(observed).__name__
            violations.append({"path": field, "error": f"expected {expected.__name__}, got {name}"})
    return violations

schema = {"id": {"type": int}, "label": {"type": str}}
print(validate({"id": "x", "label": 3}, schema))
```

## Failure Modes

| Failure Mode | Cause | Mitigation |
|---|---|---|
| Silent coercion | A wrong-typed value cast into the stream | Reject on type mismatch; never coerce silently |
| Partial acceptance | Some fields validated, others assumed | Validate the declared contract completely or not at all |
| Schema drift | Upstream changed shape and the schema did not | Version the schema; test against real samples |
| Error laundering | Failures stringified as if they were data | Failures enter as structured error records |
| Over-validation | Unused fields strictly checked, blocking good data | Schema exactly what consumers read, nothing more |

## Security and Authority Boundary

Validation is a security boundary, not just a correctness one: bounds and enum checks constrain what malformed or hostile payloads can inject into downstream logic, so schemas on tool outputs must be treated with the same review rigor as schemas on user input.

## Evidence

This skill is grounded in dated public implementation references:

1. The JSON Schema specification site (https://json-schema.org/).
2. The pandera data validation framework documentation (https://pandera.readthedocs.io/).

Honest boundary: these are implementation references, not adoption or demand evidence; this entry was added under the owner-directed corpus expansion recorded in `meta/memory/DECISIONS.md`, and no demand signal is claimed for it.

## Related Skills

- [Tool Schema Design](tool-schema-design.md) — declaring the shape tools must accept and return.
- [Function Calling](function-calling.md) — the calling layer whose outputs get validated.

## Changelog

| Date | Version | Change |
|---|---|---|
| `2026-10` | v1 | Initial entry added under the owner-directed corpus expansion |
