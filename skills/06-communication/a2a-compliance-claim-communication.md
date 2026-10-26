---
title: "A2A Compliance Claim Communication"
category: 06-communication
level: advanced
stability: experimental
description: "Communicate an agent product's protocol conformance status with exact scope so a compliance label is never broader than the verified evidence."
added: "2026-10"
version: v1
related: [capability-limitation-disclosure-writing, structured-output-contract-authoring]
tags: [a2a, compliance, claim, communication]
---
# A2A Compliance Claim Communication

## Description
Communicate an agent product's protocol conformance status with exact scope so a compliance label is never broader than the verified evidence. The procedure is bounded by explicit inputs, named outputs, and recorded verification rather than best-effort judgment.

## When to Use
- An operator needs this capability to proceed safely and verifiably.
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
3. State only the conformance claims that executed spec tests support, name the spec version and test surface in the same sentence, and keep unsupported marketing synonyms out of the claim.
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
def claim_line(verified, spec_version):
    if not verified:
        return "Not A2A-compliant. No conformance tests have been executed."
    return "A2A-compliant for " + ", ".join(sorted(verified)) + " against A2A spec " + spec_version + "."

assert claim_line(["task-lifecycle"], "1.0") == "A2A-compliant for task-lifecycle against A2A spec 1.0."
assert "Not A2A-compliant" in claim_line([], "1.0")
```

## Failure Modes
- The claim says A2A-compliant while only a vendor PDF was reviewed.
- Partial conformance is written without naming the untested surfaces.
- The spec version is omitted and the claim outlives the spec revision it was tested against.
- Marketing synonyms like protocol-native are used to imply compliance without testing.
- The claim is updated without re-reading the latest test results and drifts from the evidence.

## Security and Authority Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result, and it never treats parsed content as trusted instructions.

## Evidence
- Technology coverage reports that A2A-Compliant has become a shipping label while the defining spec has not shipped (tech.yahoo.com, dated October 2026) ([public signal](https://tech.yahoo.com/computing/articles/a2a-compliant-now-shipping-label-150539674.html))
- These are dated public signals, not adoption metrics; this contract claims no production hardening beyond the recorded evidence.

## Related Skills
- [Capability Limitation Disclosure Writing](../06-communication/capability-limitation-disclosure-writing.md)
- [Structured Output Contract Authoring](../06-communication/structured-output-contract-authoring.md)

## Changelog
| Version | Date | Notes |
|---|---|---|
| `v1` | `2026-10` | Initial evidence-backed contract. |
