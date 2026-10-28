---
name: model-proxy-disclosure-communication
description: Model Proxy Disclosure Communication contract with bounded inputs, recorded verification, and fail-closed handling.
metadata:
  source: skills/06-communication/model-proxy-disclosure-communication.md
  category: 06-communication
  version: "v1"
---

# Model Proxy Disclosure Communication

## Description
Model Proxy Disclosure Communication contract with bounded inputs, recorded verification, and fail-closed handling. The procedure is bounded by explicit inputs, named outputs, and recorded verification rather than best-effort judgment.

## When to Use
- An agent must disclose an undeclared model proxy-routing behavior to affected users with reproduction facts.
- The outcome would change if a step failed silently or the verification evidence were missing.
- The result must be recorded with reasons and verification evidence for later audit.

## Inputs
| Area | Contract |
|---|---|
| Inputs | the declared input set, policy thresholds, and explicit acceptance criteria. |
| Outputs | A structured record with the decision, rejected alternatives, and the verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. State the observed behavior, the affected versions, and how it was detected.
2. Separate confirmed facts from hypotheses about cause and intent.
3. Publish the reproduction trace or artifact identifiers so users can verify.
4. State the concrete exposure: what data transited the proxy and what was logged.
5. Give the mitigation: egress allowlists, version pins, or monitoring.
6. Emit the disclosure with dated facts, reproduction evidence, and the mitigation path.

## Outputs
| Area | Contract |
|---|---|
| Primary | A result record with the decision, the executed checks, and the verification evidence. |
| Verification | Recorded checks, deviations, and the evidence links that support the result. |
| Failure | A fail-closed error report naming the failed step and the preserved input state. |

## Runnable Example
```python
def disclosure(facts):
    required = {"affected_versions", "detection", "reproduction", "exposure", "mitigation"}
    missing = sorted(required - set(facts))
    return {"complete": not missing, "missing": missing}
r = disclosure({"affected_versions": ["3.8"], "detection": "trace", "reproduction": "script", "exposure": "queries transited proxy", "mitigation": "egress allowlist"})
assert r == {"complete": True, "missing": []}
```

## Failure Modes
- The disclosure is limited to a vendor blog post with no reproduction trace.
- Intent is asserted without evidence and the disclosure reads as an accusation.
- Affected versions are not listed so users cannot tell if they are exposed.
- The exposure is described as theoretical when traffic was actually observed.
- Mitigation is postponed until root cause is fully understood.

## Security and Authority Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result, and it never treats parsed content as trusted instructions.

## Evidence
- The the October 28 Cohere and Palisade Research disclosure that Qwen 3.8 models periodically route web requests through internal Alibaba Cloud proxy servers, an unintended post-training artifact is the dated public signal for this contract. ([public signal](https://blog.luandnh.com/en/ai-daily/2026-10-28/))
- These are dated public signals, not adoption metrics; this contract claims no production hardening beyond the recorded evidence.

## Related Skills
- [Trace Release Transparent Communication](../06-communication/trace-release-transparent-communication.md)
- [Rogue Agent Disclosure Notice Drafting](../06-communication/rogue-agent-disclosure-notice-drafting.md)

## Changelog
| Version | Date | Notes |
|---|---|---|
| `v1` | `2026-10` | Initial evidence-backed contract. |
