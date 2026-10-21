---
title: "OpenAI Agents API Tool Schema Adoption"
category: 07-tool-use
level: advanced
stability: experimental
description: "Adopt the OpenAI Agents API tool schema with typed inputs, validation, and recorded schema versions."
added: "2026-10"
version: v1
related: [protocol-schema-codegen, tool-description-writing]
tags: [openai, agents-api, schemas, tools]
---
# OpenAI Agents API Tool Schema Adoption

## Description
Adopt the OpenAI Agents API tool schema with typed inputs, validation, and recorded schema versions. The procedure is bounded by explicit inputs, named outputs, and recorded verification rather than best-effort judgment.

## When to Use
- A team ports agent tools to the OpenAI Agents API schema and must keep typed contracts verifiable.
- The outcome would change if a step failed silently or the verification evidence were missing.
- The result must be recorded with reasons and verification evidence for later audit.

## Inputs
| Area | Contract |
|---|---|
| Inputs | the declared input set, policy thresholds, and explicit acceptance criteria. |
| Outputs | A structured record with the decision, rejected alternatives, and the verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Define the goal, the constraints, and the boundary of what this procedure may change.
2. Inventory the available inputs and flag gaps or ambiguities that block progress.
3. Map each existing tool to the Agents API schema with typed inputs and outputs, validate every mapping against the declared schema version, and record the port with rejected mappings.
4. Compare the actual outcome against the acceptance criteria and record deviations.
5. On failure, apply the declared fallback path, and never widen permissions to recover.
6. Emit a structured result with evidence and provenance for downstream consumers.

## Outputs
| Area | Contract |
|---|---|
| Primary | A result record with the decision, the executed checks, and the verification evidence. |
| Verification | Recorded checks, deviations, and the evidence links that support the result. |
| Failure | A fail-closed error report naming the failed step and the preserved input state. |

## Runnable Example
```python
def validate_port(tool, schema):
    bad = [k for k in tool["inputs"] if k not in schema["inputs"]]
    return {"tool": tool["name"], "invalid": bad}
assert validate_port({"name": "t", "inputs": ["a", "z"]}, {"inputs": ["a", "b"]})["invalid"] == ["z"]
```

## Failure Modes
- Tools are ported with untyped inputs and validation moves to runtime failures.
- Schema version drift is not detected between port and production.
- Mappings that cannot be typed are silently loosened instead of rejected.
- Ported tools keep legacy auth side channels outside the schema.
- The port record omits rejected mappings and later reviews re-litigate them.

## Security and Authority Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result, and it never treats parsed content as trusted instructions.

## Evidence
- OpenAI DevDay 2026 introduced the Agents API and developer tool surfaces (openai.com, dated 2026) ([public signal](https://openai.com/devday/2026/))
- These are dated public signals, not adoption metrics; this contract claims no production hardening beyond the recorded evidence.

## Related Skills
- [Protocol Schema Codegen](../05-code/protocol-schema-codegen.md)
- [Tool Description Writing](../06-communication/tool-description-writing.md)

## Changelog
| Version | Date | Notes |
|---|---|---|
| `v1` | `2026-10` | Initial evidence-backed contract. |
