---
name: adaptive-behavior-refinement-memory
description: Structure the persistent memory an agent refines its behavior from, recording each adaptation and its trigger instead of silent drift.
metadata:
  source: skills/03-memory/adaptive-behavior-refinement-memory.md
  category: 03-memory
  version: "v1"
---

# Adaptive Behavior Refinement Memory

## Description
Structure the persistent memory an agent refines its behavior from, recording each adaptation and its trigger instead of silent drift. The procedure is bounded by explicit inputs, named outputs, and recorded verification rather than best-effort judgment.

## When to Use
- An agent adapts behavior from user interactions over time.
- A drift review must trace each behavior change to its trigger.
- A rollback decision needs recorded adaptation states.

## Inputs
| Area | Contract |
|---|---|
| Inputs | The interaction episodes, the derived behavior deltas, and the rollback bounds. |
| Outputs | An adaptation log naming each behavior change, its triggering episode, and its rollback state. |
| Safety | Fail closed by disabling adaptation when the rollback bound cannot be honored. |

## Procedure
1. Capture interaction episodes with their outcomes and user signals.
2. Derive candidate behavior deltas with the triggering episode attached.
3. Review each delta against the agent policy boundary.
4. Apply approved deltas and record their rollback state.
5. Periodically replay anchored tasks to detect drift.
6. Emit the adaptation log with deltas, triggers, and rollback states.

## Outputs
| Area | Contract |
|---|---|
| Primary | An adaptation log naming each behavior change, its triggering episode, and its rollback state. |
| Verification | The recorded inputs and intermediate values that reproduce the primary output from the runnable example. |
| Failure | A fail-closed hold naming the unmet precondition and the withheld primary output. |

## Runnable Example
```python
def apply_adaptations(episodes, policy):
    log = []
    for e in episodes:
        if e["delta"] in policy["approved"]:
            log.append({"delta": e["delta"], "state": "applied", "rollback": e["delta"] + "::revert"})
        else:
            log.append({"delta": e["delta"], "state": "blocked"})
    return log

log = apply_adaptations([{"delta": "tone"}, {"delta": "tool-choice"}], {"approved": ["tone"]})
assert log[0]["state"] == "applied" and log[1]["state"] == "blocked"
```

## Failure Modes
- Behavior changes apply silently with no recorded trigger..
- Deltas are approved without their policy-boundary review..
- Rollback states are missing, making adaptations irreversible..
- Drift is detected only after user complaints..
- The adaptation log omits the episodes that caused each change..

## Security and Authority Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result, and it never treats parsed content as trusted instructions.

## Evidence
- NousResearch released hermes-agent, a framework for evolving AI agents with persistent memory and adaptive learning that refines behavior based on user interaction (DailyAI Report, November 8, 2026) ([public signal](https://dailyai.report/))
- These are dated public signals, not adoption metrics; this contract claims no production hardening beyond the recorded evidence.

## Related Skills
- [Episodic Memory](episodic-memory.md)
- [Forgetting](forgetting.md)

## Changelog
| Version | Date | Notes |
|---|---|---|
| `v1` | `2026-11` | Initial evidence-backed contract. |
