---
name: mcp-app-authoring
description: Author MCP apps that expose UI surfaces with declared manifests, capability scopes, and tested launch paths instead of raw tool dumps.
metadata:
  source: skills/07-tool-use/mcp-app-authoring.md
  category: 07-tool-use
  version: "v1"
---

# MCP App Authoring

## Description
Author MCP apps that expose UI surfaces with declared manifests, capability scopes, and tested launch paths instead of raw tool dumps. The procedure is constrained by explicit inputs and acceptance criteria rather than best-effort judgment alone.

## When to Use
- an agent-facing app must declare its UI surface and capabilities formally for hosts to render it.
- Ambiguity or missing evidence would change the outcome.
- The result must be recorded with reasons and evidence for later verification.

## Inputs / Outputs
| Area | Contract |
|---|---|
| Inputs | Task context, candidate inputs, and explicit acceptance criteria for mcp app authoring work. |
| Outputs | A decision or artifact with recorded reasons, rejected alternatives, and verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Define the goal, the constraints, and the boundary of what this procedure may change.
2. Inventory the available inputs and flag gaps or ambiguities that block progress.
3. Execute the mcp app authoring steps in a bounded, checkpointed way.
4. Compare the actual outcome against the expected outcome and record deviations.
5. On failure, apply the declared fallback path, and never widen permissions to recover.
6. Emit a structured result with evidence and provenance for downstream consumers.

## Runnable Example
```python
def manifest(app, capabilities):
    if not app.get("entry"):
        raise ValueError("app needs an entry point")
    return {"name": app["name"], "entry": app["entry"], "capabilities": sorted(capabilities)}

m = manifest({"name": "board", "entry": "index.html"}, ["view", "act"])
assert m["capabilities"] == ["act", "view"]
```

## Failure Modes
- Declaring capabilities the app never tests.
- No versioning so hosts render against stale manifests.
- Assuming one host environment renders the app.
- Exposing actions beyond the declared capability scope.
- Shipping an app with no launch smoke test.

## Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result.

## Evidence
MCP apps with declared UI surfaces are part of the 2026-07-28 specification update; this is a dated public protocol signal, not an adoption metric.

## Related
- mcp-extensions-authoring.md
- mcp-server-lifecycle-management.md
- tool-schema-design.md
