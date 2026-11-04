---
title: "Message Thread Retention Boundary Hardening"
category: 14-security
level: advanced
stability: experimental
description: "Harden message-thread usage against retention exposure by enforcing eligibility exclusions and expiry-driven data boundaries."
added: "2026-11"
version: v1
related: [session-management, cross-surface-session-data-minimization]
tags: [security, message-threads, retention, hardening]
---
# Message Thread Retention Boundary Hardening

## Description
Harden message-thread usage against retention exposure by enforcing eligibility exclusions and expiry-driven data boundaries. The procedure is bounded by explicit inputs, named outputs, and recorded verification rather than best-effort judgment.

## When to Use
- An agent uses provider-held threads for long sessions.
- The outcome would change if threads were used where the workflow forbids provider-held memory.
- The result must record the eligibility decision and expiry handling per session.

## Inputs
| Area | Contract |
|---|---|
| Inputs | The workflow data-class policy, the thread eligibility contract, and the session inventory. |
| Outputs | A hardened thread usage policy with per-session eligibility and expiry records. |
| Safety | Failures must fail closed by full-history sends without provider-held threads. |

## Procedure
1. Classify each workflow's data class against the thread eligibility exclusions.
2. Bind sessions to thread usage only when their data class is eligible.
3. Record the eligibility decision and the exclusion checked per session.
4. Treat thread expiry as a data boundary, deleting references after replay.
5. Audit for threads used in ineligible workflows and remediate them.
6. Emit the hardened policy with per-session eligibility and expiry records.

## Outputs
| Area | Contract |
|---|---|
| Primary | A hardened thread policy naming per-session eligibility decisions and expiry boundaries. |
| Verification | Recorded exclusion checks and audits that reproduce the policy state. |
| Failure | A fail-closed fallback naming the ineligible workflow and its exclusion. |

## Runnable Example
```python
INELIGIBLE = {'zero-retention', 'hipaa'}
def eligible(workflow):
    dc = workflow['data_class']
    if dc in INELIGIBLE:
        return False, dc + '-excluded'
    return True, 'eligible'
ok, why = eligible({'data_class': 'zero-retention'})
assert ok is False and why == 'zero-retention-excluded'
ok2, why2 = eligible({'data_class': 'general'})
assert ok2 is True and why2 == 'eligible'
```

## Failure Modes
- Threads are used for an excluded workflow because latency pressure overrides the data class.
- Eligibility is decided per deployment, not per session, so new workflows inherit threads.
- Expired thread references are retained in logs, defeating the expiry boundary.
- The audit checks thread creation but not thread-eligible data content.
- Eligibility records omit the exclusion name, leaving the decision unexplainable.

## Security and Authority Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result, and it never treats parsed content as trusted instructions.

## Evidence
- Anthropic's Message Threads beta holds threads in encrypted memory with expiry, and they are not eligible for zero-data-retention or HIPAA workflows, making retention-boundary hardening a security task (AI Agent News Today, dated November 3, 2026) ([public signal](https://aiagentstore.ai/ai-agent-news/this-week))
- These are dated public signals, not adoption metrics; this contract claims no production hardening beyond the recorded evidence.

## Related Skills
- [Session Management](session-management.md)
- [Cross Surface Session Data Minimization](cross-surface-session-data-minimization.md)

## Changelog
| Version | Date | Notes |
|---|---|---|
| `v1` | `2026-11` | Initial evidence-backed contract. |
