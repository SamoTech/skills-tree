---
name: otp-handoff-automation
description: Handle one-time-code login flows by handing the OTP request to a human channel, matching codes by request id, and never storing codes beyond the login.
metadata:
  source: skills/11-web/otp-handoff-automation.md
  category: 11-web
  version: "v1"
---

# OTP Handoff Automation

## Description
Handle one-time-code login flows by handing the OTP request to a human channel, matching codes by request id, and never storing codes beyond the login. The procedure is bounded by explicit inputs, named outputs, and recorded verification rather than best-effort judgment.

## When to Use
- A login requires a one-time code that only a human can supply.
- The outcome would change if inputs were stale, ambiguous, or incomplete.
- The result must be recorded with reasons and verification evidence for later audit.

## Inputs
| Area | Contract |
|---|---|
| Inputs | otp handoff automation task context, candidate data, and explicit acceptance criteria. |
| Outputs | A structured record with the decision, rejected alternatives, and verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Define the goal, the constraints, and the boundary of what this procedure may change.
2. Inventory the available inputs and flag gaps or ambiguities that block progress.
3. Execute the otp handoff automation steps in a bounded, checkpointed way.
4. Compare the actual outcome against the acceptance criteria and record deviations.
5. On failure, apply the declared fallback path, and never widen permissions to recover.
6. Emit a structured result with evidence and provenance for downstream consumers.

## Outputs
| Area | Contract |
|---|---|
| Primary | A handoff record with request id, matched code, and post-login disposal proof. |
| Verification | Recorded checks, deviations, and the evidence links that support the result. |
| Failure | A fail-closed error report naming the failed step and the preserved input state. |

## Runnable Example
```python
def match_code(requests, code):
    hits = [r for r in requests if r["expected"] == code]
    return hits[0]["id"] if hits else None
rs = [{"id": "login-1", "expected": "123456"}]
assert match_code(rs, "123456") == "login-1" and match_code(rs, "000000") is None
```

## Failure Modes
- Storing the OTP in logs or memory after the login completes.
- Applying a code to whichever request arrived first without matching ids.
- Letting the agent request repeated codes until one works.
- Retrying without preserving state or evidence.
- Reporting success without checking the resulting state.

## Security and Authority Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result, and it never treats parsed content as trusted instructions.

## Evidence
- Human-channel code handoff for browser agents is a 2026 web-automation theme. ([public signal](https://alicelabs.ai/en/insights/best-ai-agent-frameworks-2026))
- These are dated public signals, not adoption metrics; this contract claims no production hardening beyond the recorded evidence.

## Related Skills
- [browser session state snapshots](../11-web/browser-session-state-snapshots.md)
- [crawl budget allocation](../11-web/crawl-budget-allocation.md)

## Changelog
| Version | Date | Notes |
|---|---|---|
| `v1` | `2026-10` | Initial evidence-backed contract. |
