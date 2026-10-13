---
name: webmcp-page-tool-exposure
description: Expose page capabilities as WebMCP tools with declared permissions, origin scoping, and user-consent gating so pages can serve agents safely.
metadata:
  source: skills/07-tool-use/webmcp-page-tool-exposure.md
  category: 07-tool-use
  version: "v1"
---

# WebMCP Page Tool Exposure

## Description
Expose page capabilities as WebMCP tools with declared permissions, origin scoping, and user-consent gating so pages can serve agents safely. The procedure is constrained by explicit inputs and acceptance criteria rather than best-effort judgment alone.

## When to Use
- a web page must expose its capabilities to visiting agents without giving away unscoped access.
- Ambiguity or missing evidence would change the outcome.
- The result must be recorded with reasons and evidence for later verification.

## Inputs / Outputs
| Area | Contract |
|---|---|
| Inputs | Task context, candidate inputs, and explicit acceptance criteria for webmcp page tool exposure work. |
| Outputs | A decision or artifact with recorded reasons, rejected alternatives, and verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Define the goal, the constraints, and the boundary of what this procedure may change.
2. Inventory the available inputs and flag gaps or ambiguities that block progress.
3. Execute the webmcp page tool exposure steps in a bounded, checkpointed way.
4. Compare the actual outcome against the expected outcome and record deviations.
5. On failure, apply the declared fallback path, and never widen permissions to recover.
6. Emit a structured result with evidence and provenance for downstream consumers.

## Runnable Example
```python
def expose(requested, allowed, consented):
    if not consented:
        return []
    return [t for t in requested if t in allowed]

allowed = {"read-list", "add-item"}
assert expose(["read-list", "delete-all"], allowed, True) == ["read-list"]
assert expose(["read-list"], allowed, False) == []
```

## Failure Modes
- Exposing tools that bypass page permissions.
- No origin check so any embedding page can call.
- Treating consent as permanent for the session.
- Exposing read tools that leak personal data.
- No rate limiting on exposed page tools.

## Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result.

## Evidence
Web-originated MCP exposure was publicly demonstrated in 2026 web-platform coverage; this is a dated public signal, not an adoption metric.

## Related
- browser-tool.md
- mcp-extensions-authoring.md
- web-search.md
