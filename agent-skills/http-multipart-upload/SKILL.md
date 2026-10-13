---
name: http-multipart-upload
description: Upload files as multipart requests with streaming, checksum headers, and resumable failure handling, and verify server-acknowledged bytes.
metadata:
  source: skills/04-action-execution/http-multipart-upload.md
  category: 04-action-execution
  version: "v1"
---

# HTTP Multipart Upload

## Description
Upload files as multipart requests with streaming, checksum headers, and resumable failure handling, and verify server-acknowledged bytes. The procedure is constrained by explicit inputs and acceptance criteria rather than best-effort judgment alone.

## When to Use
- large files must be uploaded through multipart HTTP endpoints before downstream steps can proceed safely.
- Ambiguity or missing evidence would change the outcome.
- The result must be recorded with reasons and evidence for later verification.

## Inputs / Outputs
| Area | Contract |
|---|---|
| Inputs | Task context, candidate inputs, and explicit acceptance criteria for http multipart upload work. |
| Outputs | A decision or artifact with recorded reasons, rejected alternatives, and verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Define the goal, the constraints, and the boundary of what this procedure may change.
2. Inventory the available inputs and flag gaps or ambiguities that block progress.
3. Execute the http multipart upload steps in a bounded, checkpointed way.
4. Compare the actual outcome against the expected outcome and record deviations.
5. On failure, apply the declared fallback path, and never widen permissions to recover.
6. Emit a structured result with evidence and provenance for downstream consumers.

## Runnable Example
```python
def boundary_check(parts, boundary):
    body = ""
    for name, content in parts:
        body += "--%s\r\nContent-Disposition: form-data; name=\"%s\"\r\n\r\n%s\r\n" % (boundary, name, content)
    body += "--%s--\r\n" % boundary
    assert body.startswith("--" + boundary)
    assert body.count("--" + boundary) == len(parts) + 1
    return len(body)

n = boundary_check([("file", "abc"), ("meta", "x")], "BOUND")
assert n > 0
```

## Failure Modes
- Sending bodies larger than memory in one buffer.
- Missing the final boundary terminator.
- Ignoring the server-acknowledged byte count.
- Resuming from zero after a partial upload.
- Not checksumming what the server actually stored.

## Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result.

## Evidence
File ingestion through HTTP APIs is a recurring 2026 integration request for agent pipelines; this is a dated signal, not an adoption metric.

## Related
- http-request.md
- api-call.md
- file-download-verification.md
