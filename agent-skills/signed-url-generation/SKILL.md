---
name: signed-url-generation
description: Generate and verify cryptographically signed URLs with expiry and scope constraints so delegated web access is bounded and auditable.
metadata:
  source: skills/11-web/signed-url-generation.md
  category: 11-web
  version: "v1"
---

# Signed URL Generation

## Description
Generate and verify cryptographically signed URLs with expiry and scope constraints so delegated web access is bounded and auditable. The procedure is constrained by explicit inputs and acceptance criteria rather than best-effort judgment alone.

## When to Use
- temporary or delegated access to a resource must be bounded and verifiable.
- Ambiguity or missing evidence would change the outcome.
- The result must be recorded with reasons and evidence for later verification.

## Inputs / Outputs
| Area | Contract |
|---|---|
| Inputs | Task context, candidate inputs, and explicit acceptance criteria for signed url generation work. |
| Outputs | A decision or artifact with recorded reasons, rejected alternatives, and verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Define the goal, the constraints, and the boundary of what this procedure may change.
2. Inventory the available inputs and flag gaps or ambiguities that block progress.
3. Execute the signed url generation steps in a bounded, checkpointed way.
4. Compare the actual outcome against the expected outcome and record deviations.
5. On failure, apply the declared fallback path, and never widen permissions to recover.
6. Emit a structured result with evidence and provenance for downstream consumers.

## Runnable Example
```python
import hashlib
def sign_path(path, expires, key):
    return hashlib.sha256(('%s|%d|%s' % (path, expires, key)).encode()).hexdigest()

sig = sign_path('/report', 1790000000, 'team-a')
assert len(sig) == 64 and sign_path('/report', 1790000000, 'team-a') == sig
assert sign_path('/report', 1790000001, 'team-a') != sig
```

## Failure Modes
- Signing URLs without expiry so access never ends.
- Leaking the signing material into logs or responses.
- Using a hash without a keyed construction.
- No scope constraint so a signed path grants the whole API.
- Not auditing which signed URLs were redeemed.

## Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result.

## Evidence
Bounded delegated access via signed URLs appears in 2026 API-security discussions; this is a dated signal, not an adoption metric.

## Related
- web-oauth-flow-handling.md
- url-normalization.md
- url-redirect-tracing.md
