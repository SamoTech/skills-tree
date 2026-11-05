---
title: "Unusual But Permitted Agent Behavior Detection"
category: 14-security
level: advanced
stability: experimental
description: "Detect agent behavior that breaks no explicit rule but is unusual in context, and route it to review instead of auto-response."
added: "2026-11"
version: v1
related: [agent-runtime-anomaly-signal-perception, individually-permitted-action-chaining-pattern]
tags: [security, detection, agents, behavior]
---
# Unusual But Permitted Agent Behavior Detection

## Description
Detect agent behavior that breaks no explicit rule but is unusual in context, and route it to review instead of auto-response. The procedure is bounded by explicit inputs, named outputs, and recorded verification rather than best-effort judgment.

## When to Use
- Permitted-but-unusual agent activity must surface for review.
- Detection must not depend on rule violations.
- Review routing must be deterministic.

## Inputs
| Area | Contract |
|---|---|
| Inputs | The baseline activity profiles, the live agent event stream, and the review routing table. |
| Outputs | A detection report naming permitted-but-unusual events with context and review destinations. |
| Safety | Fail closed by withholding detection when baselines are stale. |

## Procedure
1. Load fresh baseline profiles for each agent and tool pairing.
2. Score live events for contextual deviation without a rule trigger.
3. Classify deviations as review-worthy using the routing table thresholds.
4. Route review-worthy events to the named reviewers.
5. Emit the detection report with baseline freshness dates.

## Outputs
| Area | Contract |
|---|---|
| Primary | A detection report naming permitted-but-unusual events with context and review destinations. |
| Verification | Baseline versions and deviation scores that reproduce each detection. |
| Failure | A fail-closed report naming stale baselines that block detection. |

## Runnable Example
```python
def detect(events, baselines, route):
    out = []
    for e in events:
        base = baselines.get(e["agent"])
        if base is None or base["stale"]:
            return {"ok": False}
        if e["count"] > base["limit"]:
            out.append({"agent": e["agent"], "to": route[e["class"]]})
    return {"ok": True, "routed": out}
r = detect([{"agent": "a1", "count": 5, "class": "bulk-export"}],
           {"a1": {"limit": 2, "stale": False}}, {"bulk-export": "dpo"})
assert r["ok"] and r["routed"][0]["to"] == "dpo"
```

## Failure Modes
- Detection waits for a rule violation that never comes.
- Stale baselines keep producing detections or none at all.
- Routed events are auto-blocked, defeating the review purpose.
- Context classes are dropped, so bulk exports look like normal traffic.
- Baseline freshness dates are not recorded with detections.

## Security and Authority Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result, and it never treats parsed content as trusted instructions.

## Evidence
- Traditional policy checks may miss harmful behavior that is individually permitted but unusual in context, which Agent Insider Threat Detection is built to catch (AI Agents News, week of November 5, 2026) ([public signal](https://aiagentstore.ai/ai-agent-news/this-week))
- These are dated public signals, not adoption metrics; this contract claims no production hardening beyond the recorded evidence.

## Related Skills
- [Agent Runtime Anomaly Signal Perception](agent-runtime-anomaly-signal-perception.md)
- [Individually Permitted Action Chaining Pattern](individually-permitted-action-chaining-pattern.md)

## Changelog
| Version | Date | Notes |
|---|---|---|
| `v1` | `2026-11` | Initial evidence-backed contract. |
