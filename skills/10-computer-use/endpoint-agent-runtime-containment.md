---
title: "Endpoint Agent Runtime Containment"
category: 10-computer-use
level: advanced
stability: experimental
description: "Contain agent runtimes on endpoints by bounding processes, file access, and network paths to declared scopes."
added: "2026-11"
version: v1
related: [computer-use-privileged-action-guard, managed-cloud-agent-environment-setup]
tags: [computer-use, containment, endpoints, agents]
---
# Endpoint Agent Runtime Containment

## Description
Contain agent runtimes on endpoints by bounding processes, file access, and network paths to declared scopes. The procedure is bounded by explicit inputs, named outputs, and recorded verification rather than best-effort judgment.

## When to Use
- Agents run on endpoints alongside user sessions.
- A containment policy must bound process, file, and network scope.
- Uncontained agents are a systemic risk on staff machines.

## Inputs
| Area | Contract |
|---|---|
| Inputs | The endpoint agent runtime inventory, the declared scopes, and the containment control set. |
| Outputs | A containment state per agent naming process, file, and network bounds with control status. |
| Safety | Fail closed by blocking any agent runtime without all three bounds enforced. |

## Procedure
1. Enumerate agent runtimes on the endpoint with their processes.
2. Match each runtime to its declared scope for files and network.
3. Enforce process, file-access, and network bounds per runtime.
4. Verify each bound with an observed control state.
5. Emit the containment state and block unbounded runtimes.

## Outputs
| Area | Contract |
|---|---|
| Primary | A containment state per agent naming process, file, and network bounds with control status. |
| Verification | Observed control states that verify each enforced bound. |
| Failure | A fail-closed report naming runtimes with missing bounds. |

## Runnable Example
```python
def contain(runtimes):
    out = []
    for r in runtimes:
        ok = all(r.get(b) for b in ("proc", "file", "net"))
        out.append({"agent": r["id"], "contained": ok})
    return out
r = contain([{"id": "a1", "proc": 1, "file": 1, "net": 1}, {"id": "a2", "proc": 1}])
assert r[0]["contained"] and r[1]["contained"] is False
```

## Failure Modes
- Only network bounds are enforced, leaving file access open.
- A declared scope is recorded but never enforced.
- Uncontained runtimes keep running with a warning.
- Containment is verified once and never re-checked after updates.
- User-session boundaries are ignored, so agents act as the user.

## Security and Authority Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result, and it never treats parsed content as trusted instructions.

## Evidence
- A security advisory argues that agents on employee endpoints are becoming a systemic risk for companies and governments (AGI HUNT AI News Daily, dated November 5, 2026) ([public signal](https://agihunt.info/en/daily/2026-11-05))
- These are dated public signals, not adoption metrics; this contract claims no production hardening beyond the recorded evidence.

## Related Skills
- [Computer Use Privileged Action Guard](computer-use-privileged-action-guard.md)
- [Managed Cloud Agent Environment Setup](managed-cloud-agent-environment-setup.md)

## Changelog
| Version | Date | Notes |
|---|---|---|
| `v1` | `2026-11` | Initial evidence-backed contract. |
