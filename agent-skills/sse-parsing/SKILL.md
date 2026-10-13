---
name: sse-parsing
description: Parse server-sent event streams from MCP Streamable HTTP and other push endpoints, reassemble event ids and data frames, and handle reconnection cursors deterministically.
metadata:
  source: skills/01-perception/sse-parsing.md
  category: 01-perception
  version: "v1"
---

# Server-Sent Events Parsing

## Description
Parse server-sent event streams from MCP Streamable HTTP and other push endpoints, reassemble event ids and data frames, and handle reconnection cursors deterministically. The procedure is constrained by explicit inputs and acceptance criteria rather than best-effort judgment alone.

## When to Use
- a push endpoint delivers events as an SSE stream that must be consumed reliably before downstream steps can proceed safely.
- Ambiguity or missing evidence would change the outcome.
- The result must be recorded with reasons and evidence for later verification.

## Inputs / Outputs
| Area | Contract |
|---|---|
| Inputs | Task context, candidate inputs, and explicit acceptance criteria for sse parsing work. |
| Outputs | A decision or artifact with recorded reasons, rejected alternatives, and verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Define the goal, the constraints, and the boundary of what this procedure may change.
2. Inventory the available inputs and flag gaps or ambiguities that block progress.
3. Execute the sse parsing steps in a bounded, checkpointed way.
4. Compare the actual outcome against the expected outcome and record deviations.
5. On failure, apply the declared fallback path, and never widen permissions to recover.
6. Emit a structured result with evidence and provenance for downstream consumers.

## Runnable Example
```python
def parse_sse(block):
    events, current = [], {}
    for line in block.split("\n"):
        if line == "":
            if current.get("data") is not None:
                events.append(current)
            current = {}
        elif line.startswith("id:"):
            current["id"] = line[3:].strip()
        elif line.startswith("data:"):
            current["data"] = line[5:].strip()
    return events

stream = "id: 1\ndata: hello\n\nid: 2\ndata: world\n\n"
events = parse_sse(stream)
assert [e["id"] for e in events] == ["1", "2"]
assert events[1]["data"] == "world"
```

## Failure Modes
- Dropping the last event because its blank terminator never arrived.
- Overwriting multi-line data fields.
- Losing the last-event id on reconnect.
- Treating comment lines as data.
- Assuming events arrive in id order.

## Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result.

## Evidence
The MCP 2026-07-28 specification made Streamable HTTP the standard transport, which uses server-sent event streams; this is a dated public protocol signal, not an adoption metric.

## Related
- streaming-tool-output.md
- websocket-communication.md
- api-response-parsing.md
