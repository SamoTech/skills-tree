---
title: "Incremental JSON Parsing"
category: 01-perception
level: advanced
stability: experimental
description: "Consume partially received or streamed JSON payloads from model and tool APIs, extract only complete top-level values, and hold truncated fragments until more data arrives."
added: "2026-10"
version: v1
related: [api-response-parsing, streaming-asr-partial-parsing, structured-data-reading]
tags: [json, streaming, parsing]
---

# Incremental JSON Parsing

## Description
Consume partially received or streamed JSON payloads from model and tool APIs, extract only complete top-level values, and hold truncated fragments until more data arrives. The procedure is constrained by explicit inputs and acceptance criteria rather than best-effort judgment alone.

## When to Use
- a stream delivers JSON in chunks and downstream logic must act on complete values only before downstream steps can proceed safely.
- Ambiguity or missing evidence would change the outcome.
- The result must be recorded with reasons and evidence for later verification.

## Inputs / Outputs
| Area | Contract |
|---|---|
| Inputs | Task context, candidate inputs, and explicit acceptance criteria for incremental json parsing work. |
| Outputs | A decision or artifact with recorded reasons, rejected alternatives, and verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Define the goal, the constraints, and the boundary of what this procedure may change.
2. Inventory the available inputs and flag gaps or ambiguities that block progress.
3. Execute the incremental json parsing steps in a bounded, checkpointed way.
4. Compare the actual outcome against the expected outcome and record deviations.
5. On failure, apply the declared fallback path, and never widen permissions to recover.
6. Emit a structured result with evidence and provenance for downstream consumers.

## Runnable Example
```python
import json

def complete_values(buffer):
    out, depth, start = [], 0, None
    for i, ch in enumerate(buffer):
        if ch in "{[":
            depth += 1
            if depth == 1: start = i
        elif ch in "}]":
            depth -= 1
            if depth == 0 and start is not None:
                out.append(json.loads(buffer[start:i+1])); start = None
    return out

chunked = '{"a": 1}{"b": [2, 3]}'
assert len(complete_values(chunked)) == 2
assert complete_values('{"a": 1') == []
```

## Failure Modes
- Acting on a syntactically incomplete object.
- Losing bytes between chunks.
- Assuming chunk boundaries align with value boundaries.
- Treating a parse error as end of stream.
- Re-parsing the whole buffer per chunk and hiding O(n squared) cost.

## Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result.

## Evidence
Streamed tool and model API responses are standard in 2026 agent stacks, including MCP Streamable HTTP; this is a dated ecosystem signal, not an adoption metric.

## Related
- api-response-parsing.md
- streaming-asr-partial-parsing.md
- structured-data-reading.md
