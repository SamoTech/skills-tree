---
title: "MCP Extensions Authoring"
category: 07-tool-use
level: basic
stability: experimental
description: "Author MCP extensions using the published Extensions framework with capability declarations, backward-compatibility checks, and explicit dependency on server support."
added: "2026-10"
version: v1
related: [mcp-tool, tool-schema-design, function-calling]
tags: [mcp, extensions, authoring, tool]
---

# MCP Extensions Authoring

## Description
Author MCP extensions using the published Extensions framework with capability declarations, backward-compatibility checks, and explicit dependency on server support. The procedure is constrained by explicit inputs and acceptance criteria rather than best-effort judgment alone.

## When to Use
- The task has explicit constraints such as time, budget, or safety that must gate the outcome.
- A silent failure mode exists that must be surfaced rather than swallowed.
- Verification evidence is required before the result is trusted.

## Inputs / Outputs
| Area | Contract |
|---|---|
| Inputs | Task context, candidate inputs, and explicit acceptance criteria for mcp extensions authoring. |
| Outputs | A decision or artifact with recorded reasons, rejected alternatives, and verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Define the goal, the constraints, and the boundary of what this procedure may change.
2. Inventory the available inputs and flag gaps or ambiguities that block progress.
3. Execute the mcp extensions authoring steps in a bounded, checkpointed way.
4. Compare the actual outcome against the expected outcome and record deviations.
5. On failure, apply the declared fallback path, and never widen permissions to recover.
6. Emit a structured result with evidence and provenance for downstream consumers.

## Runnable Example
```python
# MCP Extensions Authoring: deterministic check
def validate(record, required):
    missing = [k for k in required if k not in record]
    return (True, []) if not missing else (False, missing)

ok, missing = validate({"id": "x", "source": "y"}, ["id", "source"])
assert ok and not missing
print("validated")
```

## Failure Modes
- Acting outside the declared task boundary.
- Assuming an estimate or preview equals the verified effect.
- Retrying without preserving state or evidence.
- Using stale inputs as if they were current.
- Reporting success without checking the resulting state.

## Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result.

## Evidence
The MCP 2026-07-28 specification release candidate introduces the Extensions framework; extension authoring is a dated public signal. These are dated public signals, not adoption metrics.

## Related
- mcp-tool.md
- tool-schema-design.md
- function-calling.md
