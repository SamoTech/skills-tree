---
name: agent-client-protocol-usage
description: Use agent-client protocols to expose editor integrations with declared modes, workspace scopes, and consent boundaries.
metadata:
  source: skills/07-tool-use/agent-client-protocol-usage.md
  category: 07-tool-use
  version: "v1"
---

# Agent Client Protocol Usage

## Description
Use agent-client protocols to expose editor integrations with declared modes, workspace scopes, and consent boundaries. The procedure is constrained by explicit inputs and acceptance criteria rather than best-effort judgment alone.

## When to Use
- an agent integrates with an editor or client host and must declare its mode and scope correctly.
- Ambiguity or missing evidence would change the outcome.
- The result must be recorded with reasons and evidence for later verification.

## Inputs / Outputs
| Area | Contract |
|---|---|
| Inputs | Task context, candidate inputs, and explicit acceptance criteria for agent client protocol usage work. |
| Outputs | A decision or artifact with recorded reasons, rejected alternatives, and verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Define the goal, the constraints, and the boundary of what this procedure may change.
2. Inventory the available inputs and flag gaps or ambiguities that block progress.
3. Execute the agent client protocol usage steps in a bounded, checkpointed way.
4. Compare the actual outcome against the expected outcome and record deviations.
5. On failure, apply the declared fallback path, and never widen permissions to recover.
6. Emit a structured result with evidence and provenance for downstream consumers.

## Runnable Example
```python
def negotiate(requested, supported):
    mode = next((m for m in requested if m in supported), None)
    if mode is None:
        raise ValueError("no supported mode in request")
    return mode

assert negotiate(["plan", "act"], ["ask", "act"]) == "act"
try:
    negotiate(["yolo"], ["ask", "act"])
    raise AssertionError("should have raised")
except ValueError:
    print("negotiation held")
```

## Failure Modes
- Defaulting to autonomous mode without consent.
- Declaring read-only mode while writing files.
- Ignoring the workspace root boundary the client set.
- No mode downgrade when the host revokes consent.
- Skipping the protocol version handshake.

## Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result.

## Evidence
Agent-client editor protocols like ACP saw public releases and adoption in 2026 tooling; this is a dated public signal, not an adoption metric.

## Related
- a2a-tool.md
- function-calling.md
- mcp-tool.md
