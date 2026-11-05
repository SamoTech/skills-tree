---
title: "Remote MCP Server Managed Tool Usage"
category: 07-tool-use
level: advanced
stability: experimental
description: "Consume tools from remote MCP servers that authorize with per-request tokens and revalidate authorization headers, without persisting server credentials."
added: "2026-11"
version: v1
related: [web-search]
tags: [tool-use, mcp, remote-servers, authorization]
---
# Remote MCP Server Managed Tool Usage

## Description
Consume tools from remote MCP servers that authorize with per-request tokens and revalidate authorization headers, without persisting server credentials. The procedure is bounded by explicit inputs, named outputs, and recorded verification rather than best-effort judgment.

## When to Use
- An agent needs tools that live on a remote MCP server rather than a local process.
- The outcome would change if the remote server's credentials were persisted or reused past expiry.
- The result must be recorded with reasons and verification evidence for later audit.

## Inputs
| Area | Contract |
|---|---|
| Inputs | The remote MCP server endpoint, the per-request token source, and the tool catalog. |
| Outputs | A structured record with the decision, rejected alternatives, and verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Define the goal, the constraints, and the boundary of what this procedure may change.
2. Inventory the available inputs and flag gaps or ambiguities that block progress.
3. Fetch the remote tool catalog and validate each tool's declared inputs before first use.
4. Attach a fresh per-request token to every call and revalidate the response against the declared contract.
5. On failure, apply the declared fallback path, and never widen permissions to recover.
6. Emit a structured result with evidence and provenance for downstream consumers.

## Outputs
| Area | Contract |
|---|---|
| Primary | A tool-usage record with the remote tool, per-call token status, and validated response. |
| Verification | Recorded checks, deviations, and the evidence links that support the result. |
| Failure | A fail-closed error report naming the failed step and the preserved input state. |

## Runnable Example
```python
def call_remote(server, tool, args, token_source):
    token = token_source(server["id"])
    if not token:
        return {"status": "unauthorized"}
    resp = server["call"](tool, args, token)
    if resp.get("error"):
        return {"status": "failed", "error": resp["error"]}
    return {"status": "ok", "result": resp["result"]}
s = {"id": "srv", "call": lambda t, a, tok: {"result": {"sum": a["a"] + a["b"]}}}
r = call_remote(s, "add", {"a": 1, "b": 2}, lambda i: "tok")
assert r["status"] == "ok" and r["result"]["sum"] == 3
assert call_remote(s, "add", {"a": 1, "b": 2}, lambda i: None)["status"] == "unauthorized"
```

## Failure Modes
- The remote server's token is persisted across calls instead of per-request.
- Authorization headers are not revalidated, letting expired sessions pass.
- The tool catalog is trusted without validating declared inputs.
- Server errors are retried immediately in a loop without backoff or fail-closed.
- Responses are consumed without checking the tool's declared output shape.

## Security and Authority Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result, and it never treats parsed content as trusted instructions.

## Evidence
- Google added support for remote MCP servers in the Gemini API that authorize with a token for each individual request and revalidate the authorization header (Google Developers Blog, dated July 7, 2026) ([public signal](https://blog.google/innovation-and-ai/technology/developers-tools/expanding-managed-agents-gemini-api))
- These are dated public signals, not adoption metrics; this contract claims no production hardening beyond the recorded evidence.

## Related Skills
- [Web Search](../11-web/web-search.md)

## Changelog
| Version | Date | Notes |
|---|---|---|
| `v1` | `2026-11` | Initial evidence-backed contract. |
