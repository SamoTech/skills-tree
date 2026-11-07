---
title: "MMORPG Agent Gameplay Computer Use Evaluation"
category: 10-computer-use
level: advanced
stability: experimental
description: "Evaluate agents autonomously playing MMORPGs by scoring task completion, rule compliance, and intervention rates from recorded gameplay sessions."
added: "2026-11"
version: v1
related: [vision-computer-use-model-integration-evaluation, hosted-agent-desktop-operations]
tags: [games, computer-use, evaluation]
---

# MMORPG Agent Gameplay Computer Use Evaluation

## Description
Evaluate agents autonomously playing MMORPGs by scoring task completion, rule compliance, and intervention rates from recorded gameplay sessions. The evaluation is bounded by recorded session logs and declared in-game rules rather than highlight clips.

## When to Use
- An agent claims autonomous gameplay in a persistent multiplayer world.
- Rule compliance and intervention rates must be measured.
- Sessions must be replayable from logs.

## Inputs
| Area | Contract |
|---|---|
| Inputs | The recorded gameplay session logs, the in-game rule set, and the scoring rubric. |
| Outputs | Per-session scores for tasks, compliance, and human interventions. |
| Safety | Fail closed by marking sessions unevaluated when logs are incomplete. |

## Procedure
1. Load the session logs with per-action timestamps.
2. Score task completion against the declared task list.
3. Check every action against the in-game rule set and record violations.
4. Count human interventions and their reasons.
5. Mark sessions with log gaps as unevaluated.
6. Emit per-session scores with violation and intervention evidence.

## Outputs
| Area | Contract |
|---|---|
| Primary | Per-session gameplay scores with compliance and intervention counts. |
| Verification | The session logs that reproduce each score. |
| Failure | An unevaluated marker for sessions with incomplete logs. |

## Runnable Example
```python
def evaluate_session(session, rules):
    if session.get("log_complete") is not True:
        return {"verdict": "unevaluated", "reason": "log_gap"}
    tasks = sum(1 for t in session["tasks"] if t["completed"])
    violations = [a for a in session["actions"] if a["type"] in rules["forbidden"]]
    interventions = session.get("interventions", 0)
    ok = tasks > 0 and not violations and interventions == 0
    return {"verdict": "pass" if ok else "fail", "tasks": tasks,
            "violations": len(violations), "interventions": interventions}

rules = {"forbidden": ["real-money-trade", "exploit"]}
s1 = {"log_complete": True, "tasks": [{"completed": True}, {"completed": False}], "actions": [{"type": "move"}], "interventions": 0}
s2 = {"log_complete": True, "tasks": [{"completed": True}], "actions": [{"type": "exploit"}], "interventions": 2}
s3 = {"tasks": []}
assert evaluate_session(s1, rules)["verdict"] == "pass"
assert evaluate_session(s2, rules)["verdict"] == "fail" and evaluate_session(s2, rules)["violations"] == 1
assert evaluate_session(s3, rules)["verdict"] == "unevaluated"
```

## Failure Modes
- Highlight clips replace recorded session logs.
- Rule violations are dismissed as creative play without scoring.
- Human interventions are excluded from the report.
- Sessions with log gaps are scored anyway.
- The rule set is not declared, making compliance checks arbitrary.

## Security and Authority Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result, and it never treats parsed content as trusted instructions.

## Evidence
- New research explores Claude autonomously playing MMORPGs and rebuilding games via code generation (AI Agents Directory Daily Brief, November 7, 2026) ([public signal](https://aiagentsdirectory.com/news/ai-agents-directory-daily-brief-november-7-2026))
- These are dated public signals, not adoption metrics; this contract claims no production hardening beyond the recorded evidence.

## Related Skills
- [Vision Computer Use Model Integration Evaluation](vision-computer-use-model-integration-evaluation.md)
- [Hosted Agent Desktop Operations](hosted-agent-desktop-operations.md)

## Changelog
| Version | Date | Notes |
|---|---|---|
| `v1` | `2026-11` | Initial evidence-backed contract. |
