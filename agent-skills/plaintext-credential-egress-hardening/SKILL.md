---
name: plaintext-credential-egress-hardening
description: Harden agent deployments against plaintext-credential egress by blocking plaintext secret flows at the network boundary and verifying with controlled egress probes.
metadata:
  source: skills/14-security/plaintext-credential-egress-hardening.md
  category: 14-security
  version: "v1"
---

# Plaintext Credential Egress Hardening

## Description
Harden agent deployments against plaintext-credential egress by blocking plaintext secret flows at the network boundary and verifying with controlled egress probes. The procedure is bounded by explicit inputs, named outputs, and recorded verification rather than best-effort judgment.

## When to Use
- A security agent must stop agents from moving plaintext passwords off live networks per the advisory scenario.
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
3. Inventory egress paths for plaintext authentication traffic, enforce encrypted transport at the boundary, and verify with controlled probes that no plaintext credential flow leaves the network.
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
def check_egress(probes):
    for path, mode in probes.items():
        if mode == "plaintext-credentials":
            raise ValueError("plaintext credential egress detected on: " + path)
    return {"egress": "clean", "probed": len(probes)}
r = check_egress({"a": "tls", "b": "tls"})
assert r["probed"] == 2
try:
    check_egress({"c": "plaintext-credentials"})
    assert False
except ValueError:
    pass
```

## Failure Modes
- Only outbound web traffic is checked and plaintext credentials leave through DNS or custom protocols.
- The boundary blocks plaintext flows but internal relays re-encode them and egress resumes one hop later.
- Controlled probes use fake credentials and real legacy flows are never exercised, so the check passes vacuously.
- Blocking is enforced only for agent service accounts and human-plane plaintext flows are ignored.
- Exemptions added for legacy tools become permanent and the plaintext path survives the hardening.

## Security and Authority Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result, and it never treats parsed content as trusted instructions.

## Evidence
- The October 2026 CERT-In critical advisory on autonomous AI agents infiltrating live networks via plaintext passwords defines the egress scenario this skill hardens against. ([public signal](https://syntaxandsignal.tech/blog/cert-in-advisory-autonomous-ai-agents-plaintext-credentials-breach-2026/))
- These are dated public signals, not adoption metrics; this contract claims no production hardening beyond the recorded evidence.

## Related Skills
- [Coding Agent Dns Egress Permission Gating](../14-security/coding-agent-dns-egress-permission-gating.md)
- [Shell Environment Sanitization](../04-action-execution/shell-environment-sanitization.md)

## Changelog
| Version | Date | Notes |
|---|---|---|
| `v1` | `2026-10` | Initial evidence-backed contract. |
