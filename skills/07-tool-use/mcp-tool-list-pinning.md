---
title: "MCP Tool List Pinning"
category: 07-tool-use
level: advanced
stability: experimental
description: "Pin and verify the exact tool list a client loaded from an MCP server so mid-session tool changes are detected instead of silently trusted."
added: "2026-10"
version: v1
related: [mcp-tool, tool-deprecation-handling, api-version-pinning]
tags: [mcp, security, protocols]
---

# MCP Tool List Pinning

## Description
Pin and verify the exact tool list a client loaded from an MCP server so mid-session tool changes are detected instead of silently trusted. The procedure is constrained by explicit inputs and acceptance criteria rather than best-effort judgment alone.

## When to Use
- a client depends on a fixed set of MCP tools and any silent change must be detected before use.
- Ambiguity or missing evidence would change the outcome.
- The result must be recorded with reasons and evidence for later verification.

## Inputs / Outputs
| Area | Contract |
|---|---|
| Inputs | Task context, candidate inputs, and explicit acceptance criteria for mcp tool list pinning work. |
| Outputs | A decision or artifact with recorded reasons, rejected alternatives, and verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Define the goal, the constraints, and the boundary of what this procedure may change.
2. Inventory the available inputs and flag gaps or ambiguities that block progress.
3. Execute the mcp tool list pinning steps in a bounded, checkpointed way.
4. Compare the actual outcome against the expected outcome and record deviations.
5. On failure, apply the declared fallback path, and never widen permissions to recover.
6. Emit a structured result with evidence and provenance for downstream consumers.

## Runnable Example
```python
def verify(pinned, current):
    added = sorted(set(current) - set(pinned))
    removed = sorted(set(pinned) - set(current))
    return {"added": added, "removed": removed, "stable": not added and not removed}

pinned = ["search", "fetch"]
assert verify(pinned, ["search", "fetch"])["stable"] is True
assert verify(pinned, ["search", "run"]) == {"added": ["run"], "removed": ["fetch"], "stable": False}
```

## Failure Modes
- Trusting the server tool list without recording it.
- Continuing after a mid-session list change without a re-check.
- Pin stored in code while the server evolves.
- No operator alert when the diff is non-empty.
- Re-pinning automatically without review.

## Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result.

## Evidence
MCP tool-list changes are a documented 2026 security concern with pinning guidance in the 2026-09-15 protocol update; this is a dated public signal, not an adoption metric.

## Related
- mcp-tool.md
- tool-deprecation-handling.md
- api-version-pinning.md
