---
name: websocket-communication
description: Establish and maintain WebSocket sessions with framing-correct message handling, heartbeat keepalives, reconnect with bounded backoff, and explicit close-code interpretation.
metadata:
  source: skills/07-tool-use/websocket-communication.md
  category: 07-tool-use
  version: "v1"
---

# WebSocket Communication

Category: Tool Use | Level: intermediate | Stability: experimental | Version: v1

## Description

The WebSocket protocol upgrades an HTTP connection into a long-lived, bidirectional message channel. Unlike a single HTTP call, a session lives for minutes or hours, so the real engineering is in staying healthy: heartbeats, bounded reconnect backoff, close-code interpretation, and queues that do not grow without limit.

## When to Use

Use when the remote endpoint provides a WebSocket API and the workload is genuinely streaming or bidirectional: live feeds, telemetry, interactive tool protocols.

Prefer ordinary HTTP for one-shot request/response; a session adds failure modes, not value.

## Inputs

| Input | Type | Required | Description |
|---|---|---|---|
| `url` | `uri` | Yes | `wss://` endpoint (never `ws://` over untrusted networks) |
| `handlers` | `map` | Yes | Callbacks per message type |
| `heartbeat_interval` | `int` | No | Ping cadence in seconds (default 30) |

## Procedure

1. Open the handshake and validate the negotiated subprotocol against the one you expect.
2. Route incoming frames through handlers; answer server pings automatically.
3. Send heartbeats on the configured cadence and treat a missed pong as a dead session, not a busy one.
4. On abnormal close, reconnect with exponential backoff and jitter; cap the delay and the total retry budget.
5. Interpret close codes precisely: 1000 is a normal close with no retry, 1006 is abnormal (no close frame), 1011 is a server error that may not be retryable.
6. Bound both send and receive queues; drop or fail explicitly rather than buffering without limit.

## Outputs

| Output | Type | Description |
|---|---|---|
| `session_state` | `enum` | `open`, `reconnecting`, `closed` with last close code |
| `delivered` | `list` | Messages sent with server acknowledgment, where the protocol provides one |
| `close_summary` | `object` | Final close code, reason, and reconnect attempts |

## Runnable Example

```python
def next_backoff(attempt, base=0.5, cap=30.0):
    """Bounded exponential backoff with a hard ceiling."""
    return min(base * (2 ** min(attempt, 6)), cap)

def interpret_close(code):
    table = {1000: "normal", 1006: "abnormal", 1011: "server_error"}
    return table.get(code, "other")

print([round(next_backoff(n), 2) for n in range(5)], interpret_close(1006))
```

## Failure Modes

| Failure Mode | Cause | Mitigation |
|---|---|---|
| Silent half-open session | Connection died without a close frame | Heartbeat pings; dead sessions detected in one interval |
| Reconnect storm | All clients retry in lockstep | Jittered backoff with a cap |
| Close code misread | 1006/1011 treated as clean close | Map close codes explicitly and record them |
| Unbounded queueing | Slow consumer during a fast stream | Bound queues; apply explicit overflow policy |
| Order assumptions across reconnects | Reconnect creates a new session | Use sequence numbers or re-sync state after reconnect |

## Security and Authority Boundary

Use `wss://` everywhere outside localhost; `ws://` is plaintext. Validate the Origin on the server side, treat every inbound frame as untrusted input, and never reconnect with credentials that the endpoint should no longer hold.

## Evidence

This skill is grounded in dated public implementation references:

1. The websockets Python library (https://pypi.org/project/websockets/).
2. RFC 6455, The WebSocket Protocol (https://datatracker.ietf.org/doc/html/rfc6455).

Honest boundary: these are implementation references, not adoption or demand evidence; this entry was added under the owner-directed corpus expansion recorded in `meta/memory/DECISIONS.md`, and no demand signal is claimed for it.

## Related Skills

- [Streaming Tool Output](streaming-tool-output.md) — presenting the streamed messages to the consuming model.
- [Function Calling](function-calling.md) — the request/response tool pattern to prefer when a session adds no value.

## Changelog

| Date | Version | Change |
|---|---|---|
| `2026-10` | v1 | Initial entry added under the owner-directed corpus expansion |
