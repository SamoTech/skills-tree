---
name: streaming-tool-output
description: Consume tool output as it arrives — newline-delimited chunks, incremental parsers, bounded buffers — so long-running results become usable before they finish.
metadata:
  source: skills/07-tool-use/streaming-tool-output.md
  category: 07-tool-use
  version: "v1"
---

# Streaming Tool Output

Category: Tool Use | Level: intermediate | Stability: experimental | Version: v1

## Description

Some tool calls are streams pretending to be calls: search results that arrive page by page, logs that emit lines for minutes, models that produce tokens before the sentence is done. This skill treats the output as a sequence with a protocol — a delimiter or an event frame — and consumes it incrementally: parse what has arrived, hold a bounded remainder for the incomplete tail, and surface progress to whoever is waiting. The alternative is buffering everything, which turns a long result into a long silence followed by a large object.

## When to Use

Use for long-running or high-volume tool output — event streams, incremental search, anything that delivers value before completion.

Do not add streaming machinery to short, fast calls; a buffered read of a small response is simpler and equally correct.

## Inputs

| Input | Type | Required | Description |
|---|---|---|---|
| `stream` | `iterator` | Yes | The tool output arriving incrementally |
| `delimiter` | `string` | Yes | The boundary that separates records, newline by default |
| `handler` | `callable` | Yes | What to run on each complete record as it parses |
| `buffer_limit` | `integer` | No | Maximum bytes held for an incomplete tail |

## Procedure

1. Fix the protocol first: know what delimits a record — a newline, a frame header, a terminator — before reading a byte.
2. Read incrementally and split on the delimiter, keeping the incomplete tail in a buffer rather than discarding it.
3. Dispatch each complete record to the handler immediately, so downstream work overlaps with the remaining stream.
4. Bound the buffer: a tail that grows past its limit is a protocol violation, and streaming must fail loudly, not allocate quietly.
5. Surface progress — records seen, bytes read — so a slow stream is observable while it runs.
6. Handle terminal conditions distinctly: end-of-stream, error frame, and cancellation are different events and must close differently.

## Outputs

| Output | Type | Description |
|---|---|---|
| `records` | `iterator` | Complete records yielded as they parse |
| `progress` | `map` | Records and bytes consumed so far |
| `close_reason` | `enum` | Terminal state of the stream when it ends |

## Runnable Example

```python
def parse_lines(chunks):
    buffer = ""
    for chunk in chunks:
        buffer += chunk
        while "\n" in buffer:
            line, buffer = buffer.split("\n", 1)
            yield line
    if buffer:
        yield buffer

def count_events(chunks):
    total = 0
    for record in parse_lines(chunks):
        total += 1
    return total

chunks = ["event-a\neve", "nt-b\nevent-c\n"]
print("events:", count_events(chunks))
```

## Failure Modes

| Failure Mode | Cause | Mitigation |
|---|---|---|
| Split records | A record divided across chunk boundaries | Buffer the incomplete tail and split on the delimiter |
| Unbounded buffering | A stream with no delimiters fills memory | Enforce a buffer limit and fail loudly on overflow |
| Lost tails | Final unterminated record dropped at close | Yield the remainder when the stream ends |
| Blocked consumers | Slow handler stalls the entire stream | Dispatch records and let the consumer set pace |
| Ambiguous closes | Error, cancel, and completion all look alike | Close with an explicit terminal reason per stream |

## Security and Authority Boundary

Streamed output bypasses the size checks that whole responses get: incremental data must still be validated per record at the boundary, and progress events must not leak record contents into logs where whole payloads would never be allowed.

## Evidence

This skill is grounded in dated public implementation references:

1. The JSON Lines format specification site (https://jsonlines.org/).
2. Wikipedia's overview of stream processing (https://en.wikipedia.org/wiki/Stream_processing).

Honest boundary: these are implementation references, not adoption or demand evidence; this entry was added under the owner-directed corpus expansion recorded in `meta/memory/DECISIONS.md`, and no demand signal is claimed for it.

## Related Skills

- [Function Calling](function-calling.md) — the call layer that can deliver results incrementally.
- [MCP Tool](mcp-tool.md) — a concrete protocol whose outputs can stream.

## Changelog

| Date | Version | Change |
|---|---|---|
| `2026-10` | v1 | Initial entry added under the owner-directed corpus expansion |
