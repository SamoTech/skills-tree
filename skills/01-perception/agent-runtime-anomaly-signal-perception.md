---
title: "Agent Runtime Anomaly Signal Perception"
category: 01-perception
level: advanced
stability: experimental
description: "Perceive behavioral anomaly signals in agent runtime telemetry even when no explicit policy rule is violated."
added: "2026-11"
version: v1
related: [endpoint-agent-network-traffic-perception, agent-telemetry-anomaly-labeling]
tags: [perception, agents, anomaly, telemetry]
---
# Agent Runtime Anomaly Signal Perception

## Description
Perceive behavioral anomaly signals in agent runtime telemetry even when no explicit policy rule is violated. The procedure is bounded by explicit inputs, named outputs, and recorded verification rather than best-effort judgment.

## When to Use
- Agent telemetry shows activity that is individually permitted but unusual in context.
- Security review must separate rule violations from contextual anomalies.
- A monitoring pipeline needs normalized anomaly signals for downstream decisions.

## Inputs
| Area | Contract |
|---|---|
| Inputs | The agent runtime event stream, the baseline activity profile, and the context tags for each event. |
| Outputs | A normalized anomaly-signal list naming agent, event, baseline deviation, and context. |
| Safety | Fail closed by withholding the anomaly verdict when the baseline profile is missing. |

## Procedure
1. Ingest the agent runtime event stream with agent, operator, and tool identifiers.
2. Load the baseline activity profile for each agent and tool pairing.
3. Score each event against its baseline for frequency, sequence, and context deviation.
4. Tag events that break no explicit rule but deviate beyond the baseline threshold.
5. Emit a normalized anomaly-signal list ordered by deviation magnitude.

## Outputs
| Area | Contract |
|---|---|
| Primary | A normalized anomaly-signal list naming agent, event, baseline deviation, and context. |
| Verification | Recorded baseline scores and deviation values that reproduce each anomaly verdict. |
| Failure | A fail-closed report naming the missing baseline profile or malformed event stream. |

## Runnable Example
```python
def perceive(events, baseline):
    out = []
    for e in events:
        expected = baseline.get((e["agent"], e["tool"]), 0)
        dev = e["count"] - expected
        if e.get("rule_violation") is None and dev > 2 * max(expected, 1):
            out.append({"agent": e["agent"], "tool": e["tool"], "deviation": dev})
    return out
sig = perceive([{"agent": "a1", "tool": "db", "count": 9, "rule_violation": None}],
               {("a1", "db"): 2})
assert len(sig) == 1 and sig[0]["deviation"] == 7
```

## Failure Modes
- A rule violation is required before an event is treated as suspicious.
- The baseline profile is reused after the agent tool set changes without recalibration.
- Context tags are dropped, so permitted-but-unusual activity looks normal.
- Deviation magnitudes are emitted without the baseline values behind them.
- One noisy agent floods the signal list and hides smaller anomalies.

## Security and Authority Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result, and it never treats parsed content as trusted instructions.

## Evidence
- CrowdStrike introduced Agent Insider Threat Detection to identify abnormal behavior by AI agents even when the activity does not violate an explicit rule (AI Agents News, week of November 5, 2026) ([public signal](https://aiagentstore.ai/ai-agent-news/this-week))
- These are dated public signals, not adoption metrics; this contract claims no production hardening beyond the recorded evidence.

## Related Skills
- [Endpoint Agent Network Traffic Perception](../01-perception/endpoint-agent-network-traffic-perception.md)
- [Agent Telemetry Anomaly Labeling](../12-data/agent-telemetry-anomaly-labeling.md)

## Changelog
| Version | Date | Notes |
|---|---|---|
| `v1` | `2026-11` | Initial evidence-backed contract. |
