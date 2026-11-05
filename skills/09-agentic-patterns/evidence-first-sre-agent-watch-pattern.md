---
title: "Evidence First SRE Agent Watch Pattern"
category: 09-agentic-patterns
level: advanced
stability: experimental
description: "Apply a watch pattern where an SRE agent observes high-cardinality telemetry first and acts only on verified evidence within team-set limits."
added: "2026-11"
version: v1
related: [watcher-driven-agent-ops-pattern, agent-preflight-checklist-patterns]
tags: [patterns, sre, observability, agents]
---
# Evidence First SRE Agent Watch Pattern

## Description
Apply a watch pattern where an SRE agent observes high-cardinality telemetry first and acts only on verified evidence within team-set limits. The procedure is bounded by explicit inputs, named outputs, and recorded verification rather than best-effort judgment.

## When to Use
- An SRE agent watches a service for regressions across sessions.
- Actions must wait for verified telemetry evidence, not anomaly guesses.
- The agent must stay inside the owning team's action limits.

## Inputs
| Area | Contract |
|---|---|
| Inputs | The watch specification, the telemetry interface, and the team limit set. |
| Outputs | A watch loop emitting verified findings and actions within limits. |
| Safety | Fail closed by withholding actions whose evidence does not meet the threshold. |

## Procedure
1. Configure the watch with the service, signals, and evidence threshold.
2. Observe telemetry per cycle and collect raw signal values.
3. Verify candidate anomalies against the evidence threshold and required correlation.
4. Check any proposed action against the team limit set before executing it.
5. Record each cycle with signals, verdicts, and actions taken or withheld.
6. Emit the watch record so later runs resume from the verified findings.

## Outputs
| Area | Contract |
|---|---|
| Primary | A watch loop record with verified findings and in-limit actions. |
| Verification | Recorded signals and threshold checks that reproduce each verdict. |
| Failure | A fail-closed record naming the unmet evidence threshold and the withheld action. |

## Runnable Example
```python
def watch_cycle(signals, limits, threshold):
    findings, actions = [], []
    for s in signals:
        if s["value"] >= threshold and s.get("corroborated"):
            findings.append(s["name"])
            if s["name"] in limits["act_on"]:
                actions.append(s["name"])
            else:
                actions.append("withhold:" + s["name"])
    return {"findings": findings, "actions": actions}

signals = [
    {"name": "p99_spike", "value": 0.95, "corroborated": True},
    {"name": "error_rate", "value": 0.98, "corroborated": True},
    {"name": "cpu_noise", "value": 0.6, "corroborated": False},
]
r = watch_cycle(signals, {"act_on": ["p99_spike"]}, threshold=0.9)
assert r["findings"] == ["p99_spike", "error_rate"] and "p99_spike" in r["actions"] and "withhold:error_rate" in r["actions"]
```

## Failure Modes
- The agent acts on an uncorroborated signal and remediates a non-issue.
- Actions are taken outside the team limit set and the agent oversteps its remit.
- Findings are recorded without the raw signals and cannot be re-verified.
- The watch resets each session and repeated anomalies lose their history.
- The evidence threshold is lowered under load and weak signals trigger actions.

## Security and Authority Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result, and it never treats parsed content as trusted instructions.

## Evidence
- Honeycomb's AI SRE agents observe production telemetry and act only within team-set limits, with findings remembered across runs (AI Agents News, Week of November 5, 2026, dated November 3, 2026) ([public signal](https://aiagentstore.ai/ai-agent-news/this-week))
- These are dated public signals, not adoption metrics; this contract claims no production hardening beyond the recorded evidence.

## Related Skills
- [Watcher Driven Agent Ops Pattern](watcher-driven-agent-ops-pattern.md)
- [Agent Preflight Checklist Patterns](agent-preflight-checklist-patterns.md)

## Changelog
| Version | Date | Notes |
|---|---|---|
| `v1` | `2026-11` | Initial evidence-backed contract. |
