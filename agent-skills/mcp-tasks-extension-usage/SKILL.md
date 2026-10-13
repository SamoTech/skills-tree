---
name: mcp-tasks-extension-usage
description: Use long-running task handles from the MCP Tasks extension with polling budgets, cancellation, and result verification so remote work is not left running unbounded.
metadata:
  source: skills/07-tool-use/mcp-tasks-extension-usage.md
  category: 07-tool-use
  version: "v1"
---

# MCP Tasks Extension Usage

## Description
Use long-running task handles from the MCP Tasks extension with polling budgets, cancellation, and result verification so remote work is not left running unbounded. The procedure is constrained by explicit inputs and acceptance criteria rather than best-effort judgment alone.

## When to Use
- a tool call runs longer than a request and the task handle must be managed deliberately.
- Ambiguity or missing evidence would change the outcome.
- The result must be recorded with reasons and evidence for later verification.

## Inputs / Outputs
| Area | Contract |
|---|---|
| Inputs | Task context, candidate inputs, and explicit acceptance criteria for mcp tasks extension usage work. |
| Outputs | A decision or artifact with recorded reasons, rejected alternatives, and verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Define the goal, the constraints, and the boundary of what this procedure may change.
2. Inventory the available inputs and flag gaps or ambiguities that block progress.
3. Execute the mcp tasks extension usage steps in a bounded, checkpointed way.
4. Compare the actual outcome against the expected outcome and record deviations.
5. On failure, apply the declared fallback path, and never widen permissions to recover.
6. Emit a structured result with evidence and provenance for downstream consumers.

## Runnable Example
```python
def poll(handle_log, budget_ms, elapsed_ms):
    if handle_log["status"] == "completed":
        return "result"
    if elapsed_ms > budget_ms:
        return "cancel"
    return "continue"

log = {"status": "running"}
assert poll({"status": "completed"}, 1000, 500) == "result"
assert poll(log, 1000, 5000) == "cancel"
```

## Failure Modes
- Polling forever with no deadline.
- Losing the task handle so it runs unbounded.
- Treating a completed handle as a successful one without checking errors.
- No cancellation on client shutdown.
- Assuming the extension is present without negotiating it.

## Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result.

## Evidence
The MCP Tasks extension for long-running work shipped in the 2026-07-28 specification update; this is a dated public protocol signal, not an adoption metric.

## Related
- mcp-extensions-authoring.md
- mcp-tool.md
- tool-behavior-contract-testing.md
