---
name: consumer-agent-privacy-complaint-response
description: Respond to consumer privacy complaints about agent data access with a factual ingest record and a concrete remediation offer.
metadata:
  source: skills/16-domain-specific/consumer-agent-privacy-complaint-response.md
  category: 16-domain-specific
  version: "v1"
---
# Consumer Agent Privacy Complaint Response

## Description
Respond to consumer privacy complaints about agent data access with a factual ingest record and a concrete remediation offer. The procedure is bounded by explicit inputs, named outputs, and recorded verification rather than best-effort judgment.

## When to Use
- A consumer complains that an agent accessed their data and the response must be factual and remedial.
- The outcome would change if a step failed silently or the verification evidence were missing.
- The result must be recorded with reasons and verification evidence for later audit.

## Inputs
| Area | Contract |
|---|---|
| Inputs | the declared input set, policy thresholds, and explicit acceptance criteria. |
| Outputs | A structured record with the decision, rejected alternatives, and the verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Define the goal, the constraints, and the boundary of what this procedure may change.
2. Inventory the available inputs and flag gaps or ambiguities that block progress.
3. Retrieve the ingest record for the complainant scope, state what was accessed from the record rather than policy, and offer the concrete remediation of revocation and deletion with its limits.
4. Compare the actual outcome against the acceptance criteria and record deviations.
5. On failure, apply the declared fallback path, and never widen permissions to recover.
6. Emit a structured result with evidence and provenance for downstream consumers.

## Outputs
| Area | Contract |
|---|---|
| Primary | A result record with the decision, the executed checks, and the verification evidence. |
| Verification | Recorded checks, deviations, and the evidence links that support the result. |
| Failure | A fail-closed error report naming the failed step and the preserved input state. |

## Runnable Example
```python
def respond(complaint, ingest_record):
    accessed = ingest_record.get(complaint["scope"], [])
    reply = {
        "accessed_count": len(accessed),
        "remediation": ["revoke_access", "delete_ingested"],
        "limits": "derived summaries may persist until manual purge",
    }
    if complaint["scope"] not in ingest_record:
        reply["limits"] = "no record found; scope never ingested"
    return reply

rec = {"messages": [1, 2]}
out = respond({"scope": "messages"}, rec)
assert out["accessed_count"] == 2 and "revoke_access" in out["remediation"]
assert respond({"scope": "photos"}, rec)["accessed_count"] == 0
```

## Failure Modes
- The response states policy instead of the actual ingest record.
- Accessed counts are rounded so the scale reads smaller.
- Revocation is offered without acknowledging already-ingested data.
- Deletion is offered for raw records but not derived summaries.
- Complaints are answered with a template that names the wrong scope.

## Security and Authority Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result, and it never treats parsed content as trusted instructions.

## Evidence
- Associated Press reporting records consumer confusion and complaints about agent access to messages and personal data, making factual complaint response a dated live need (apnews.com, dated October 19, 2026) ([public signal](https://apnews.com/article/meta-muse-openai-dot-ai-privacy-449734d41d3750aad7038b761faa49c9))
- These are dated public signals, not adoption metrics; this contract claims no production hardening beyond the recorded evidence.

## Related Skills
- [Incident Response](../16-domain-specific/incident-response.md)
- [Merchant Agent Commerce Dispute Operations](../16-domain-specific/merchant-agent-commerce-dispute-operations.md)

## Changelog
| Version | Date | Notes |
|---|---|---|
| `v1` | `2026-10` | Initial evidence-backed contract. |
