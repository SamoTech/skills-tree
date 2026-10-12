---
title: "Agent Eval Harness Design"
category: 09-agentic-patterns
level: advanced
stability: experimental
description: "Design an evaluation harness for an agent with explicit cases, metrics, thresholds, and failure labels, so runs are reproducible and comparable over time."
added: "2026-10"
version: v1
related: [skill-quality-evaluation, agent-observability-tracing, critic-agent]
tags: [agent, eval, harness, design, agentic]
---

# Agent Eval Harness Design

## Description
Design an evaluation harness for an agent with explicit cases, metrics, thresholds, and failure labels, so runs are reproducible and comparable over time. The procedure is constrained by explicit inputs and acceptance criteria rather than best-effort judgment alone.

## When to Use
- Multiple inputs or candidates compete and must be resolved by explicit criteria.
- A wrong intermediate result would propagate into consequential actions.
- The task repeats and benefits from a deterministic procedure.

## Inputs / Outputs
| Area | Contract |
|---|---|
| Inputs | Task context, candidate inputs, and explicit acceptance criteria for agent eval harness design. |
| Outputs | A decision or artifact with recorded reasons, rejected alternatives, and verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Normalize the task into explicit inputs, constraints, and acceptance criteria.
2. Gather the required evidence and check completeness before proceeding.
3. Apply the agent eval harness design procedure using the declared criteria only.
4. Record the outcome, rejected alternatives, and the reason for each rejection.
5. Verify the result against the acceptance criteria with an independent check.
6. Report the result with evidence, and escalate explicitly when a criterion cannot be met.

## Runnable Example
```python
# Agent Eval Harness Design: deterministic check
options = [{"name": "x", "gain": 5, "cost": 1}, {"name": "y", "gain": 4, "cost": 1}]
ranked = sorted(options, key=lambda o: (o["cost"], -o["gain"]))
assert ranked[0]["name"] == "x"
print("best:", ranked[0]["name"])
```

## Failure Modes
- Proceeding with agent eval harness design without the required evidence or inputs.
- Treating an unverified result as verified.
- Silently swallowing errors instead of failing closed with reasons.
- Optimizing the stated metric while violating the stated constraint.
- Losing the audit trail of decisions and rejected alternatives.

## Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result.

## Evidence
Agent evaluation is the top reported 2026 developer pain point in public community threads; harness design requests recur across framework issues. These are dated public signals, not adoption metrics.

## Related
- skill-quality-evaluation.md
- agent-observability-tracing.md
- critic-agent.md
