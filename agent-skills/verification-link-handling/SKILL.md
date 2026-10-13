---
name: verification-link-handling
description: Consume email verification links during automated flows with expiry, single-use, and replay checks before treating an account as verified.
metadata:
  source: skills/11-web/verification-link-handling.md
  category: 11-web
  version: "v1"
---

# Verification Link Handling

## Description
Consume email verification links during automated flows with expiry, single-use, and replay checks before treating an account as verified. The procedure is constrained by explicit inputs and acceptance criteria rather than best-effort judgment alone.

## When to Use
- an automated flow must complete an email verification step safely.
- Ambiguity or missing evidence would change the outcome.
- The result must be recorded with reasons and evidence for later verification.

## Inputs / Outputs
| Area | Contract |
|---|---|
| Inputs | Task context, candidate inputs, and explicit acceptance criteria for verification link handling work. |
| Outputs | A decision or artifact with recorded reasons, rejected alternatives, and verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Define the goal, the constraints, and the boundary of what this procedure may change.
2. Inventory the available inputs and flag gaps or ambiguities that block progress.
3. Execute the verification link handling steps in a bounded, checkpointed way.
4. Compare the actual outcome against the expected outcome and record deviations.
5. On failure, apply the declared fallback path, and never widen permissions to recover.
6. Emit a structured result with evidence and provenance for downstream consumers.

## Runnable Example
```python
def consume_link(link, used, expires, now):
    if now > expires:
        return 'expired'
    if link in used:
        return 'replayed'
    used.add(link)
    return 'verified'

used = set()
assert consume_link('l1', used, 100, 50) == 'verified'
assert consume_link('l1', used, 100, 60) == 'replayed'
assert consume_link('l2', used, 100, 200) == 'expired'
```

## Failure Modes
- Treating a click as verification without checking the response.
- Reusing a link after it was already consumed.
- Ignoring expiry and processing stale links.
- Accepting links from the wrong sender or domain.
- Recording verification without keeping the link provenance.

## Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result.

## Evidence
Automated verification-link consumption with replay protection recurs in 2026 account-flow requests; this is a dated signal, not an adoption metric.

## Related
- web-login.md
- url-fetching.md
- url-redirect-tracing.md
