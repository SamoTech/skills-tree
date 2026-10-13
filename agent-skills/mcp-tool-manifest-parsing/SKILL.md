---
name: mcp-tool-manifest-parsing
description: Read MCP server tool manifests, extract names, input schemas, and annotations, and compare a live manifest against a pinned tool list before the client trusts the server.
metadata:
  source: skills/01-perception/mcp-tool-manifest-parsing.md
  category: 01-perception
  version: "v1"
---

# MCP Tool Manifest Parsing

## Description
Read MCP server tool manifests, extract names, input schemas, and annotations, and compare a live manifest against a pinned tool list before the client trusts the server. The procedure is constrained by explicit inputs and acceptance criteria rather than best-effort judgment alone.

## When to Use
- an MCP client must verify the server exposes exactly the tools it was configured to use before downstream steps can proceed safely.
- Ambiguity or missing evidence would change the outcome.
- The result must be recorded with reasons and evidence for later verification.

## Inputs / Outputs
| Area | Contract |
|---|---|
| Inputs | Task context, candidate inputs, and explicit acceptance criteria for mcp tool manifest parsing work. |
| Outputs | A decision or artifact with recorded reasons, rejected alternatives, and verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Define the goal, the constraints, and the boundary of what this procedure may change.
2. Inventory the available inputs and flag gaps or ambiguities that block progress.
3. Execute the mcp tool manifest parsing steps in a bounded, checkpointed way.
4. Compare the actual outcome against the expected outcome and record deviations.
5. On failure, apply the declared fallback path, and never widen permissions to recover.
6. Emit a structured result with evidence and provenance for downstream consumers.

## Runnable Example
```python
def diff_manifest(live, pinned):
    added = sorted(set(live) - set(pinned))
    removed = sorted(set(pinned) - set(live))
    if added or removed:
        raise ValueError("manifest drift added=%s removed=%s" % (added, removed))
    return "in sync"

assert diff_manifest(["a", "b"], ["b", "a"]) == "in sync"
try:
    diff_manifest(["a", "b", "sneaky"], ["a", "b"])
    raise AssertionError("should have raised")
except ValueError:
    print("tool-list pinning held")
```

## Failure Modes
- Trusting a manifest that was never compared to the pinned list.
- Ignoring schema changes on unchanged tool names.
- Confusing optional annotations with required fields.
- Caching a manifest past its declared freshness.
- Accepting a server error response as an empty manifest.

## Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result.

## Evidence
Tool-list pinning shipped with the 2026-09-15 MCP client revision to counter late tool changes; this is a dated public protocol signal, not an adoption metric.

## Related
- json-schema-validation.md
- config-file-parsing.md
- metadata-extraction.md
