---
name: electronic-signature-automation
description: Automate electronic signature capture and placement flows with identity, document-integrity, and audit-trail checks enforced before signing.
metadata:
  source: skills/10-computer-use/electronic-signature-automation.md
  category: 10-computer-use
  version: "v1"
---

# Electronic Signature Automation

## Description
Automate electronic signature capture and placement flows with identity, document-integrity, and audit-trail checks enforced before signing. The procedure is constrained by explicit inputs and acceptance criteria rather than best-effort judgment alone.

## When to Use
- a document signing flow must be automated without weakening identity or integrity checks.
- Ambiguity or missing evidence would change the outcome.
- The result must be recorded with reasons and evidence for later verification.

## Inputs / Outputs
| Area | Contract |
|---|---|
| Inputs | Task context, candidate inputs, and explicit acceptance criteria for electronic signature automation work. |
| Outputs | A decision or artifact with recorded reasons, rejected alternatives, and verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Define the goal, the constraints, and the boundary of what this procedure may change.
2. Inventory the available inputs and flag gaps or ambiguities that block progress.
3. Execute the electronic signature automation steps in a bounded, checkpointed way.
4. Compare the actual outcome against the expected outcome and record deviations.
5. On failure, apply the declared fallback path, and never widen permissions to recover.
6. Emit a structured result with evidence and provenance for downstream consumers.

## Runnable Example
```python
def sign_guard(doc_hash, signer_id, consent):
    if not (doc_hash and signer_id and consent):
        raise ValueError('signature preconditions unmet')
    return {'doc': doc_hash, 'signer': signer_id, 'consent': consent}

s = sign_guard('abc123', 'user-7', True)
assert s['signer'] == 'user-7'
```

## Failure Modes
- Signing a document whose hash was never verified.
- Proceeding without recorded signer consent.
- Losing the audit trail entry for an applied signature.
- Signing the wrong document version from a stale copy.
- Treating signature placement as proof of legal validity.

## Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result.

## Evidence
E-signature flow automation with audit evidence is a recurring 2026 document-workflow request; this is a dated signal, not an adoption metric.

## Related
- desktop-app-testing.md
- file-dialog.md
- computer-use-error-recovery.md
