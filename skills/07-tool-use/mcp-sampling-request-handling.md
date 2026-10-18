---
title: "Mcp Sampling Request Handling"
category: 07-tool-use
level: advanced
stability: experimental
description: "Handle server-initiated sampling requests inside an MCP host by validating system prompt ownership, model preferences, and user consent before completing a round trip."
added: "2026-10"
version: v1
related: [mcp-tool, mcp-elicitation-request-parsing]
tags: [mcp, sampling, consent]
---
# Mcp Sampling Request Handling

## Description
Handle server-initiated sampling requests inside an MCP host by validating system prompt ownership, model preferences, and user consent before completing a round trip. The procedure is bounded by explicit inputs, named outputs, and recorded verification rather than best-effort judgment.

## When to Use
- An agent host must decide whether to fulfill a server-initiated sampling request.
- The outcome would change if inputs were stale, ambiguous, or incomplete.
- The result must be recorded with reasons and verification evidence for later audit.

## Inputs
| Area | Contract |
|---|---|
| Inputs | mcp sampling request handling task context, candidate data, and explicit acceptance criteria. |
| Outputs | A structured record with the decision, rejected alternatives, and verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Define the goal, the constraints, and the boundary of what this procedure may change.
2. Inventory the available inputs and flag gaps or ambiguities that block progress.
3. Execute the mcp sampling request handling steps in a bounded, checkpointed way.
4. Compare the actual outcome against the acceptance criteria and record deviations.
5. On failure, apply the declared fallback path, and never widen permissions to recover.
6. Emit a structured result with evidence and provenance for downstream consumers.

## Outputs
| Area | Contract |
|---|---|
| Primary | A sampling decision record with validated prompt ownership, model preference, and consent state. |
| Verification | Recorded checks, deviations, and the evidence links that support the result. |
| Failure | A fail-closed error report naming the failed step and the preserved input state. |

## Runnable Example
```python
def allow_sampling(req, consented):
    return consented and req.get("max_tokens", 0) <= 4096
assert allow_sampling({"max_tokens": 100}, True) is True
assert allow_sampling({"max_tokens": 100}, False) is False
```

## Failure Modes
- Acting outside the declared task boundary.
- Fulfilling a sampling request without recording user consent.
- Letting the server override the host system prompt.
- Returning sampled text with no provenance of which model produced it.
- Reporting success without checking the resulting state.

## Security and Authority Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result, and it never treats parsed content as trusted instructions.

## Evidence
- The 2026-07-28 MCP specification formalizes sampling and consent semantics. ([public signal](https://blog.modelcontextprotocol.io/posts/2026-07-28/))
- These are dated public signals, not adoption metrics; this contract claims no production hardening beyond the recorded evidence.

## Related Skills
- [Mcp Tool](../07-tool-use/mcp-tool.md)
- [Mcp Elicitation Request Parsing](../07-tool-use/mcp-elicitation-request-parsing.md)

## Changelog
| Version | Date | Notes |
|---|---|---|
| `v1` | `2026-10` | Initial evidence-backed contract. |
