---
title: "Protocol Schema Codegen"
category: 05-code
level: advanced
stability: experimental
description: "Generate typed client bindings from protocol schemas with pinned schema versions, and verify round-trip serialization against the source schema."
added: "2026-10"
version: v1
related: [api-client-generation, sql-query-generation, type-annotation-generation]
tags: [codegen, protocols, schema]
---

# Protocol Schema Codegen

## Description
Generate typed client bindings from protocol schemas with pinned schema versions, and verify round-trip serialization against the source schema. The procedure is constrained by explicit inputs and acceptance criteria rather than best-effort judgment alone.

## When to Use
- client code must be generated from a protocol schema so manual drift between schema and code is prevented.
- Ambiguity or missing evidence would change the outcome.
- The result must be recorded with reasons and evidence for later verification.

## Inputs / Outputs
| Area | Contract |
|---|---|
| Inputs | Task context, candidate inputs, and explicit acceptance criteria for protocol schema codegen work. |
| Outputs | A decision or artifact with recorded reasons, rejected alternatives, and verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Define the goal, the constraints, and the boundary of what this procedure may change.
2. Inventory the available inputs and flag gaps or ambiguities that block progress.
3. Execute the protocol schema codegen steps in a bounded, checkpointed way.
4. Compare the actual outcome against the expected outcome and record deviations.
5. On failure, apply the declared fallback path, and never widen permissions to recover.
6. Emit a structured result with evidence and provenance for downstream consumers.

## Runnable Example
```python
def gen_bindings(schema):
    if schema.get("version") is None:
        raise ValueError("schema version required")
    return {m["name"]: m["type"] for m in schema["methods"]}

schema = {"version": "1.2", "methods": [{"name": "ping", "type": "request"}]}
b = gen_bindings(schema)
assert b == {"ping": "request"}
try:
    gen_bindings({"methods": []})
    raise AssertionError("should have raised")
except ValueError:
    print("version pin held")
```

## Failure Modes
- Generating from a schema with no recorded version.
- Hand-editing generated code that the next run overwrites.
- No round-trip test between code types and the schema.
- Generating against a moving latest schema tag.
- Ignoring deprecation markers in the schema.

## Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result.

## Evidence
Schema-first code generation for agent protocols is a recurring 2026 tooling request in public developer discussion; this is a dated signal, not an adoption metric.

## Related
- api-client-generation.md
- sql-query-generation.md
- type-annotation-generation.md
