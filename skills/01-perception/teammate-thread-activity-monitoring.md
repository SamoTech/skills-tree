---
title: "Teammate Thread Activity Monitoring"
category: 01-perception
level: advanced
stability: experimental
description: "Perceive always-on teammate agent activity by reading dedicated per-agent threads and summarizing progress, errors, and pending approvals."
added: "2026-11"
version: v1
related: [text-message-shopping-command-parsing, always-on-agent-project-context-persistence]
tags: [monitoring, teammates, threads]
---

# Teammate Thread Activity Monitoring

## Description
Perceive always-on teammate agent activity by reading dedicated per-agent threads and summarizing progress, errors, and pending approvals. The summary is bounded by explicit activity events and recorded thread state rather than inferred intent.

## When to Use
- Multiple persistent agents run in parallel and must be supervised.
- Each agent reports into a dedicated thread that a human reads periodically.
- Errors and pending approvals must surface before they block work.

## Inputs
| Area | Contract |
|---|---|
| Inputs | The per-agent thread event streams and the review policy. |
| Outputs | An activity digest naming per-agent status, errors, and pending approvals. |
| Safety | Fail closed by marking agents with missing events as unverified rather than assumed idle. |

## Procedure
1. Collect the event stream for each monitored agent thread.
2. Classify each event as progress, error, or approval request.
3. Detect silent threads by comparing the latest event time against the activity budget.
4. Rank agents by pending-approval urgency, then by error count.
5. Mark unverified any agent whose stream is incomplete or out of order.
6. Emit the activity digest with per-agent status and evidence pointers.

## Outputs
| Area | Contract |
|---|---|
| Primary | A per-agent activity digest with status, errors, and pending approvals. |
| Verification | Event identifiers and thread references that reproduce the digest. |
| Failure | An unverified marker with the missing-event reason when a stream is incomplete. |

## Runnable Example
```python
def digest(streams, now, budget=30):
    out = []
    for name, events in sorted(streams.items()):
        last = max((e["t"] for e in events), default=None)
        if last is None or now - last > budget:
            out.append({"agent": name, "status": "unverified", "reason": "silent"})
            continue
        errs = sum(1 for e in events if e["kind"] == "error")
        pend = sum(1 for e in events if e["kind"] == "approval")
        out.append({"agent": name, "status": "active", "errors": errs, "pending": pend})
    return out

s = {"a": [{"t": 10, "kind": "progress"}], "b": [{"t": 1, "kind": "approval"}]}
d = digest(s, now=12)
assert d[0] == {"agent": "a", "status": "active", "errors": 0, "pending": 0}
assert d[1] == {"agent": "b", "status": "unverified", "reason": "silent"}
```

## Failure Modes
- Silent agents are reported as idle without evidence.
- Approval requests are summarized without their thread reference.
- Events are aggregated across agents, hiding per-agent failure.
- The activity budget is not recorded with the digest.
- Digests are generated from memory of past runs instead of fresh events.

## Security and Authority Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result, and it never treats parsed content as trusted instructions.

## Evidence
- Perplexity Teammates let users run agents simultaneously, monitor them in dedicated threads, and interact through Slack (AI Agent News Today, November 7, 2026) ([public signal](https://aiagentstore.ai/ai-agent-news/daily/2026-11-07))
- These are dated public signals, not adoption metrics; this contract claims no production hardening beyond the recorded evidence.

## Related Skills
- [Text Message Shopping Command Parsing](text-message-shopping-command-parsing.md)
- [Always On Agent Project Context Persistence](always-on-agent-project-context-persistence.md)

## Changelog
| Version | Date | Notes |
|---|---|---|
| `v1` | `2026-11` | Initial evidence-backed contract. |
