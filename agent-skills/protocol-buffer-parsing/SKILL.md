---
name: protocol-buffer-parsing
description: Decode length-delimited protobuf records from wire captures and gRPC or A2A bindings into inspectable field sets without generated stubs, and flag undecodable segments instead of guessing.
metadata:
  source: skills/01-perception/protocol-buffer-parsing.md
  category: 01-perception
  version: "v1"
---

# Protocol Buffer Parsing

## Description
Decode length-delimited protobuf records from wire captures and gRPC or A2A bindings into inspectable field sets without generated stubs, and flag undecodable segments instead of guessing. The procedure is constrained by explicit inputs and acceptance criteria rather than best-effort judgment alone.

## When to Use
- a binary protocol exchange must be inspected without the original schema before downstream steps can proceed safely.
- Ambiguity or missing evidence would change the outcome.
- The result must be recorded with reasons and evidence for later verification.

## Inputs / Outputs
| Area | Contract |
|---|---|
| Inputs | Task context, candidate inputs, and explicit acceptance criteria for protocol buffer parsing work. |
| Outputs | A decision or artifact with recorded reasons, rejected alternatives, and verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Define the goal, the constraints, and the boundary of what this procedure may change.
2. Inventory the available inputs and flag gaps or ambiguities that block progress.
3. Execute the protocol buffer parsing steps in a bounded, checkpointed way.
4. Compare the actual outcome against the expected outcome and record deviations.
5. On failure, apply the declared fallback path, and never widen permissions to recover.
6. Emit a structured result with evidence and provenance for downstream consumers.

## Runnable Example
```python
def read_varint(buf, pos):
    shift, result = 0, 0
    while True:
        b = buf[pos]; pos += 1
        result |= (b & 0x7F) << shift
        if not b & 0x80:
            return result, pos
        shift += 7
        if shift > 35:
            raise ValueError("varint too long")

buf = bytes([0xAC, 0x02])
val, pos = read_varint(buf, 0)
assert val == 300 and pos == 2
try:
    read_varint(bytes([0x80] * 6), 0)
    raise AssertionError("should have raised")
except ValueError:
    print("varint guard held")
```

## Failure Modes
- Guessing field semantics without a schema.
- Silently skipping undecodable segments.
- Conflicting wire-type assumptions across records.
- Ignoring truncated trailing records.
- Treating a decoded guess as verified structure.

## Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result.

## Evidence
A2A 1.0 ships gRPC and JSON bindings for agent-to-agent traffic; protobuf payloads are a dated 2026 protocol surface, not an adoption metric.

## Related
- binary-file-reading.md
- network-traffic-reading.md
- api-response-parsing.md
