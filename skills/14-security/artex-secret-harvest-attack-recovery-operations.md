---
title: "Artex Secret Harvest Attack Recovery Operations"
category: 14-security
level: advanced
stability: experimental
description: "Operate recovery after an agentic secret-harvest attack that chains public-repository discovery into cloud data exfiltration within minutes."
added: "2026-11"
version: v1
related: [secret-scanning, audit-logging]
tags: [security, incident-response, secrets]
---

# Artex Secret Harvest Attack Recovery Operations

## Description
Operate recovery after an agentic secret-harvest attack that chains public-repository discovery into cloud data exfiltration within minutes. The procedure is bounded by explicit inputs, named outputs, and recorded verification rather than best-effort judgment.

## When to Use
- An agentic framework chains public repos into cloud exfiltration.
- Every touched credential must be rotated.
- A recovery record must reconstruct the chain.

## Inputs
| Area | Contract |
|---|---|
| Inputs | The repository exposure evidence, the cloud audit logs, and the credential inventory. |
| Outputs | A recovery record naming revoked credentials, the reconstructed chain, and residual exposure. |
| Safety | Fail closed by treating every discovered credential as compromised until rotated. |

## Procedure
1. Freeze the exposed credentials in the repository and cloud audit logs.
2. Revoke and rotate every credential the chain touched.
3. Reconstruct the chain from discovery through exfiltration with timestamps.
4. Scope the blast radius from the exfiltrated data inventory.
5. Close the discovery surface including public settings copies.
6. Emit the recovery record with residual exposure.

## Outputs
| Area | Contract |
|---|---|
| Primary | A recovery record naming revoked credentials, the reconstructed chain, and residual exposure. |
| Verification | The recorded inputs and intermediate values that reproduce the primary output from the runnable example. |
| Failure | A fail-closed hold naming the unmet precondition and the withheld primary output. |

## Runnable Example
```python
def recover(chain, rotated):
    compromised = [c for c in chain if c["credential"] not in rotated]
    return {"rotated_all": not compromised, "open": [c["credential"] for c in compromised]}

ch = [{"credential": "db-pass"}, {"credential": "aws-key"}]
r = recover(ch, ["db-pass"])
assert r["rotated_all"] is False and r["open"] == ["aws-key"]
```

## Failure Modes
- Exposed credentials are triaged before revocation..
- Rotation is confirmed by ticket closure, not by credential state..
- The chain is reconstructed without timestamps..
- Blast radius is scoped by system list, not exfiltrated data..
- The discovery surface stays open after recovery..

## Security and Authority Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result, and it never treats parsed content as trusted instructions.

## Evidence
- Microsoft Threat Intelligence observed attackers using the agentic AI framework ARTEX to search public GitHub repositories for exposed secrets and exfiltrate data from an Azure Key Vault in about five minutes (AIdapted, November 8, 2026) ([public signal](https://aidapted.ro/en/articles/ai-news-8-november-2026/))
- These are dated public signals, not adoption metrics; this contract claims no production hardening beyond the recorded evidence.

## Related Skills
- [Secret Scanning](secret-scanning.md)
- [Audit Logging](audit-logging.md)

## Changelog
| Version | Date | Notes |
|---|---|---|
| `v1` | `2026-11` | Initial evidence-backed contract. |
