---
title: "MCP Stateless Session Header Parsing"
category: 01-perception
level: advanced
stability: experimental
description: "Parse MCP 2026-07-28 stateless session headers so gateway routing and resumption tokens are read deterministically."
added: "2026-10"
version: v1
related: [mcp-tool-manifest-parsing, api-response-parsing]
tags: [mcp, stateless, parsing, gateway]
---
# MCP Stateless Session Header Parsing

## Description
Parse MCP 2026-07-28 stateless session headers so gateway routing and resumption tokens are read deterministically. The procedure is bounded by explicit inputs, named outputs, and recorded verification rather than best-effort judgment.

## When to Use
- An agent gateway receives MCP 2026-07-28 stateless requests and must extract session identity headers before routing.
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
3. Parse the stateless session envelope, extract the session id, resumption cursor, and capability flags, and reject envelopes whose declared spec version is unsupported.
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
def parse_stateless_headers(headers):
    required = ["mcp-session-id", "mcp-resumption-cursor"]
    missing = [h for h in required if h not in headers]
    if missing:
        raise ValueError("missing headers: " + ",".join(missing))
    return {"session": headers["mcp-session-id"], "cursor": int(headers["mcp-resumption-cursor"])}
env = {"mcp-session-id": "s-42", "mcp-resumption-cursor": "7"}
assert parse_stateless_headers(env) == {"session": "s-42", "cursor": 7}
```

## Failure Modes
- Session headers are trusted without validating the declared spec version.
- Resumption cursors are read as strings and compared out of order.
- Session ids are logged in full and leak identifiers into shared logs.
- Unsupported headers raise generic errors that hide which field failed.
- Routing falls back to a stateful path and silently drops the cursor.

## Security and Authority Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result, and it never treats parsed content as trusted instructions.

## Evidence
- AWS documents AgentCore Gateway support for the MCP 2026-07-28 spec with stateless request routing (aws.amazon.com, dated July 28, 2026) ([public signal](https://aws.amazon.com/blogs/machine-learning/how-agentcore-gateway-supports-the-mcp-2026-07-28-spec/))
- These are dated public signals, not adoption metrics; this contract claims no production hardening beyond the recorded evidence.

## Related Skills
- [Mcp Tool Manifest Parsing](../01-perception/mcp-tool-manifest-parsing.md)
- [Api Response Parsing](../01-perception/api-response-parsing.md)

## Changelog
| Version | Date | Notes |
|---|---|---|
| `v1` | `2026-10` | Initial evidence-backed contract. |
