---
title: "Preflight Credential Check Verification"
category: 14-security
level: advanced
stability: experimental
description: "Verify preflight credential checks in integration jobs by proving credentials are validated before dispatch and never echoed in logs."
added: "2026-11"
version: v1
related: [cross-surface-session-data-minimization, case-evidence-retention-enforcement]
tags: [security, credentials, preflight, verification]
---
# Preflight Credential Check Verification

## Description
Verify preflight credential checks in integration jobs by proving credentials are validated before dispatch and never echoed in logs. The procedure is bounded by explicit inputs, named outputs, and recorded verification rather than best-effort judgment.

## When to Use
- A credentialed integration job must prove it checks credentials before every dispatch.
- The outcome would change if a job dispatched with stale credentials and logged them on failure.
- The result must be recorded with reasons and verification evidence for later audit.

## Inputs
| Area | Contract |
|---|---|
| Inputs | The integration job definition, the credential store binding, and the failure log capture. |
| Outputs | A verification record with preflight hits and log leak findings. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Inspect the job definition for its credential store binding and dispatch order.
2. Exercise the job with a valid credential and confirm the preflight check runs first.
3. Exercise the job with a stale credential and confirm it stops before dispatch.
4. Capture the failure logs from the stale run and scan for credential material.
5. Scan the diagnostic output paths for credential echoes from any step.
6. Emit the verification record with the pass or fail per check and the log evidence.

## Outputs
| Area | Contract |
|---|---|
| Primary | A verification record proving the preflight check runs before dispatch and that failure logs contain no credential material. |
| Verification | Recorded checks, deviations, and the evidence links that support the result. |
| Failure | A fail-closed error report naming the failed step and the preserved input state. |

## Runnable Example
```python
def verify_preflight(runs):
    preflight_first = all(r["sequence"][0] == "preflight" for r in runs)
    leaks = [r["id"] for r in runs if "credential" in r["logs"]]
    return {"ok": preflight_first and not leaks, "leaks": leaks}
r = verify_preflight([{"id": "j1", "sequence": ["preflight", "dispatch"], "logs": "timeout at step 2"}])
assert r["ok"] is True and r["leaks"] == []
```

## Failure Modes
- The preflight check runs after dispatch and the ordering is never verified.
- Stale-credential failures retry with the same credential instead of stopping.
- Failure logs are assumed clean and never scanned for credential echoes.
- Only the happy path is exercised, so stale behavior is untested.
- The verification record asserts safety without log evidence attached.

## Security and Authority Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result, and it never treats parsed content as trusted instructions.

## Evidence
- GitHub’s Agentic Workflows v0.93.x releases adding preflight credential checks and improved failure diagnostics for safer handling of network and credential usage in integration jobs (AI Agent News Today, dated November 2, 2026) ([public signal](https://aiagentstore.ai/ai-agent-news/this-week))
- These are dated public signals, not adoption metrics; this contract claims no production hardening beyond the recorded evidence.

## Related Skills
- [Cross Surface Session Data Minimization](cross-surface-session-data-minimization.md)
- [Case Evidence Retention Enforcement](case-evidence-retention-enforcement.md)

## Changelog
| Version | Date | Notes |
|---|---|---|
| `v1` | `2022026-11` | Initial evidence-backed contract. |
