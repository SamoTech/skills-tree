---
title: "Release Tracker Page Diff Subscription"
category: 11-web
level: advanced
stability: experimental
description: "Subscribe to vendor release pages and diff them on a schedule, recording only substantive version changes."
added: "2026-10"
version: v1
related: [page-diff-monitoring, vendor-release-changelog-signal-parsing]
tags: [release, tracker, diff, subscription]
---
# Release Tracker Page Diff Subscription

## Description
Subscribe to vendor release pages and diff them on a schedule, recording only substantive version changes. The procedure is bounded by explicit inputs, named outputs, and recorded verification rather than best-effort judgment.

## When to Use
- A web agent must detect a new release on a vendor page that publishes no feed.
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
3. Fetch the tracked pages on schedule, diff the current snapshot against the previous one, and record substantive version changes while ignoring layout noise.
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
def diff_pages(prev, curr):
    changes = []
    for version, note in curr.items():
        if version not in prev:
            changes.append({"version": version, "note": note})
    return changes
c = diff_pages({"1.24.0": "tool approval"}, {"1.24.0": "tool approval", "1.25.0": "channels"})
assert c == [{"version": "1.25.0", "note": "channels"}]
```

## Failure Modes
- Layout changes are recorded as releases and the diff log fills with noise.
- The previous snapshot is overwritten before diffing and a missed cycle loses the baseline.
- Version strings are normalized away and patch releases are missed entirely.
- The subscription runs without rate limits and the vendor blocks the agent.
- Detected releases are recorded without the fetch timestamp and cadence analysis breaks.

## Security and Authority Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result, and it never treats parsed content as trusted instructions.

## Evidence
- The October 2026 agent framework update trackers are the dated release pages this diff subscription watches. ([public signal](https://releasebot.io/updates/microsoft/agent-framework))
- These are dated public signals, not adoption metrics; this contract claims no production hardening beyond the recorded evidence.

## Related Skills
- [Page Diff Monitoring](../11-web/page-diff-monitoring.md)
- [Vendor Release Changelog Signal Parsing](../01-perception/vendor-release-changelog-signal-parsing.md)

## Changelog
| Version | Date | Notes |
|---|---|---|
| `v1` | `2026-10` | Initial evidence-backed contract. |
