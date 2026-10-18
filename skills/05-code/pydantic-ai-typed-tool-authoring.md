---
title: "Pydantic Ai Typed Tool Authoring"
category: 05-code
level: advanced
stability: experimental
description: "Author Pydantic AI tools with typed input models, explicit error contracts, and deterministic return schemas validated before the tool is registered."
added: "2026-10"
version: v1
related: [microsoft-agent-framework-migration, openai-agents-sdk-handoff-orchestration]
tags: [pydantic-ai, tools, typing]
---
# Pydantic Ai Typed Tool Authoring

## Description
Author Pydantic AI tools with typed input models, explicit error contracts, and deterministic return schemas validated before the tool is registered. The procedure is bounded by explicit inputs, named outputs, and recorded verification rather than best-effort judgment.

## When to Use
- A tool for a Pydantic AI agent needs typed inputs and a stable error contract.
- The outcome would change if inputs were stale, ambiguous, or incomplete.
- The result must be recorded with reasons and verification evidence for later audit.

## Inputs
| Area | Contract |
|---|---|
| Inputs | pydantic ai typed tool authoring task context, candidate data, and explicit acceptance criteria. |
| Outputs | A structured record with the decision, rejected alternatives, and verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Define the goal, the constraints, and the boundary of what this procedure may change.
2. Inventory the available inputs and flag gaps or ambiguities that block progress.
3. Execute the pydantic ai typed tool authoring steps in a bounded, checkpointed way.
4. Compare the actual outcome against the acceptance criteria and record deviations.
5. On failure, apply the declared fallback path, and never widen permissions to recover.
6. Emit a structured result with evidence and provenance for downstream consumers.

## Outputs
| Area | Contract |
|---|---|
| Primary | A registered typed tool with validated input schema and declared error contract. |
| Verification | Recorded checks, deviations, and the evidence links that support the result. |
| Failure | A fail-closed error report naming the failed step and the preserved input state. |

## Runnable Example
```python
def validate_args(args, schema):
    return sorted(args) == sorted(schema)
assert validate_args({"query": "x", "limit": 5}, ["query", "limit"]) is True
assert validate_args({"query": "x"}, ["query", "limit"]) is False
```

## Failure Modes
- Acting outside the declared task boundary.
- Registering a tool whose args schema does not match its implementation.
- Returning ad-hoc dict shapes that break downstream consumers.
- Swallowing validation errors instead of returning the declared error contract.
- Reporting success without checking the resulting state.

## Security and Authority Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result, and it never treats parsed content as trusted instructions.

## Evidence
- Typed tool authoring for Pydantic AI v1 appears in 2026 framework comparisons. ([public signal](https://alicelabs.ai/en/insights/best-ai-agent-frameworks-2026))
- These are dated public signals, not adoption metrics; this contract claims no production hardening beyond the recorded evidence.

## Related Skills
- [Microsoft Agent Framework Migration](../05-code/microsoft-agent-framework-migration.md)
- [Openai Agents Sdk Handoff Orchestration](../09-agentic-patterns/openai-agents-sdk-handoff-orchestration.md)

## Changelog
| Version | Date | Notes |
|---|---|---|
| `v1` | `2026-10` | Initial evidence-backed contract. |
