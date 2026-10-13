---
name: a2a-signed-agent-card-verification
description: Verify signed A2A Agent Cards by checking the signature against a trusted key set, freshness window, and capability claims before routing work.
metadata:
  source: skills/07-tool-use/a2a-signed-agent-card-verification.md
  category: 07-tool-use
  version: "v1"
---

# A2A Signed Agent Card Verification

## Description
Verify signed A2A Agent Cards by checking the signature against a trusted key set, freshness window, and capability claims before routing work. The procedure is constrained by explicit inputs and acceptance criteria rather than best-effort judgment alone.

## When to Use
- a remote agent presents a signed card and its authenticity must be verified before any delegation.
- Ambiguity or missing evidence would change the outcome.
- The result must be recorded with reasons and evidence for later verification.

## Inputs / Outputs
| Area | Contract |
|---|---|
| Inputs | Task context, candidate inputs, and explicit acceptance criteria for a2a signed agent card verification work. |
| Outputs | A decision or artifact with recorded reasons, rejected alternatives, and verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Define the goal, the constraints, and the boundary of what this procedure may change.
2. Inventory the available inputs and flag gaps or ambiguities that block progress.
3. Execute the a2a signed agent card verification steps in a bounded, checkpointed way.
4. Compare the actual outcome against the expected outcome and record deviations.
5. On failure, apply the declared fallback path, and never widen permissions to recover.
6. Emit a structured result with evidence and provenance for downstream consumers.

## Runnable Example
```python
def verify_card(card, trusted_keys, now, max_age_s):
    if card["key_id"] not in trusted_keys:
        return "untrusted-key"
    if now - card["issued"] > max_age_s:
        return "stale"
    return "trusted"

keys = {"k1"}
assert verify_card({"key_id": "k1", "issued": 100}, keys, 150, 300) == "trusted"
assert verify_card({"key_id": "k2", "issued": 100}, keys, 150, 300) == "untrusted-key"
```

## Failure Modes
- Routing on the card fields without checking the signature.
- Accepting a valid signature from an untrusted key.
- Caching a card past its freshness window.
- Ignoring mismatch between signed and advertised capabilities.
- No fallback when verification cannot be performed.

## Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result.

## Evidence
A2A 1.0 made signed Agent Cards the discovery artifact for agent interop on 2026-03-12; this is a dated public protocol signal, not an adoption metric.

## Related
- a2a-agent-card-authoring.md
- a2a-tool.md
- tool-source-vetting.md
