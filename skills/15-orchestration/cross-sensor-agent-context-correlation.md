---
title: "Cross Sensor Agent Context Correlation"
category: 15-orchestration
level: advanced
stability: experimental
description: "Correlate what an agent was told, what it communicated, and what it executed across sensors into one agent context record."
added: "2026-11"
version: v1
related: [agent-level-hook-policy-enforcement, endpoint-agent-network-traffic-perception]
tags: [orchestration, correlation, sensors, agents]
---
# Cross Sensor Agent Context Correlation

## Description
Correlate what an agent was told, what it communicated, and what it executed across sensors into one agent context record. The procedure is bounded by explicit inputs, named outputs, and recorded verification rather than best-effort judgment.

## When to Use
- A single sensor view must be assembled from prompt, network, and endpoint telemetry.
- Root-cause analysis needs one correlated record per agent action.
- Correlation must handle clock and identifier differences across sensors.

## Inputs
| Area | Contract |
|---|---|
| Inputs | The prompt-side hook logs, the network inspection logs, and the endpoint execution logs with identifiers. |
| Outputs | A correlated per-agent context record linking told, communicated, and executed events. |
| Safety | Fail closed by marking uncorrelated events as orphaned instead of dropping them. |

## Procedure
1. Normalize identifiers and clocks across the three sensor feeds.
2. Group events by agent identity and execution chain.
3. Link told, communicated, and executed events into one record.
4. Mark events that cannot be linked as orphaned with their sensor source.
5. Emit the correlated record with coverage per sensor.

## Outputs
| Area | Contract |
|---|---|
| Primary | A correlated per-agent context record linking told, communicated, and executed events. |
| Verification | Link tables that reproduce the correlated record from raw feeds. |
| Failure | A fail-closed report naming orphaned events and missing sensor feeds. |

## Runnable Example
```python
def correlate(told, comm, executed, ids):
    rec = []
    for a in ids:
        rec.append({"agent": a, "told": told.get(a), "communicated": comm.get(a),
                    "executed": executed.get(a)})
    orphans = [a for a in ids if any(r[k] is None for k in ("told", "communicated", "executed")) for r in rec if r["agent"] == a]
    return {"records": rec, "orphans": orphans}
c = correlate({"a1": "p"}, {"a1": "net"}, {}, ["a1"])
assert c["records"][0]["executed"] is None and c["orphans"] == ["a1"]
```

## Failure Modes
- Clock skew is ignored, so events link in the wrong order.
- Unlinkable events are dropped instead of marked orphaned.
- Correlation assumes one agent per host.
- Sensor coverage is reported without feed health.
- The correlated record is treated as forensic proof without raw links.

## Security and Authority Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result, and it never treats parsed content as trusted instructions.

## Evidence
- Falcon Guardian connects what an agent is told, what it communicates, and what it executes on a single sensor to provide full context (CrowdStrike press release, dated November 3, 2026) ([public signal](https://www.crowdstrike.com/en-us/press-releases/crowdstrike-delivers-ai-security-safety-for-the-enterprise/))
- These are dated public signals, not adoption metrics; this contract claims no production hardening beyond the recorded evidence.

## Related Skills
- [Agent Level Hook Policy Enforcement](agent-level-hook-policy-enforcement.md)
- [Endpoint Agent Network Traffic Perception](endpoint-agent-network-traffic-perception.md)

## Changelog
| Version | Date | Notes |
|---|---|---|
| `v1` | `2026-11` | Initial evidence-backed contract. |
