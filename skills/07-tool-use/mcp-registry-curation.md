---
title: "MCP Registry Curation"
category: 07-tool-use
level: advanced
stability: experimental
description: "Curate server registries with health checks, capability vetting, and provenance records so teams install servers from a maintained allowlist."
added: "2026-10"
version: v1
related: [tool-inventory-cataloging, tool-source-vetting, mcp-tool]
tags: [mcp, registries, vetting]
---

# MCP Registry Curation

## Description
Curate server registries with health checks, capability vetting, and provenance records so teams install servers from a maintained allowlist. The procedure is constrained by explicit inputs and acceptance criteria rather than best-effort judgment alone.

## When to Use
- servers are pulled from registries and entries must be vetted before teams depend on them.
- Ambiguity or missing evidence would change the outcome.
- The result must be recorded with reasons and evidence for later verification.

## Inputs / Outputs
| Area | Contract |
|---|---|
| Inputs | Task context, candidate inputs, and explicit acceptance criteria for mcp registry curation work. |
| Outputs | A decision or artifact with recorded reasons, rejected alternatives, and verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Define the goal, the constraints, and the boundary of what this procedure may change.
2. Inventory the available inputs and flag gaps or ambiguities that block progress.
3. Execute the mcp registry curation steps in a bounded, checkpointed way.
4. Compare the actual outcome against the expected outcome and record deviations.
5. On failure, apply the declared fallback path, and never widen permissions to recover.
6. Emit a structured result with evidence and provenance for downstream consumers.

## Runnable Example
```python
def vet(entry):
    problems = []
    if not entry.get("provenance"):
        problems.append("no-provenance")
    if entry.get("health") != "passing":
        problems.append("unhealthy")
    return problems or ["approved"]

e = {"name": "s", "provenance": "org/x", "health": "passing"}
assert vet(e) == ["approved"]
assert vet({"name": "s", "health": "failing"}) == ["no-provenance", "unhealthy"]
```

## Failure Modes
- Listing servers with no health check.
- No provenance so anyone can register a lookalike.
- Never re-checking entries after listing.
- No removal process for abandoned servers.
- Recommending unvetted servers to users.

## Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result.

## Evidence
MCP server registries and curation are a recurring 2026 ecosystem-safety topic in public coverage; this is a dated signal, not an adoption metric.

## Related
- tool-inventory-cataloging.md
- tool-source-vetting.md
- mcp-tool.md
