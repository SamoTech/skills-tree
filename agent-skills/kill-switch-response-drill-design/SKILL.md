---
name: kill-switch-response-drill-design
description: Design and run kill-switch response drills so operators rehearse emergency agent shutdown decisions, execution, and review with recorded evidence.
metadata:
  source: skills/14-security/kill-switch-response-drill-design.md
  category: 14-security
  version: "v1"
---

# Kill Switch Response Drill Design

## Description
Design and run kill-switch response drills so operators rehearse emergency agent shutdown decisions, execution, and review with recorded evidence. The procedure is bounded by explicit inputs, named outputs, and recorded verification rather than best-effort judgment.

## When to Use
- Operators must rehearse emergency agent shutdown decisions before a real incident.
- Drill outcomes must be recorded so gaps in authorization, execution, or review are found.
- A kill-switch policy rollout must be validated by exercise rather than by assertion.

## Inputs
| Area | Contract |
|---|---|
| Inputs | The kill-switch policy, the drill scenario set, and the operator roster. |
| Outputs | A drill report naming rehearsed decisions, execution gaps, and review findings. |
| Safety | Fail closed by running drills against isolated drill agents, never production agents. |

## Procedure
1. Read the kill-switch policy and list the decision, invocation, and review steps it defines.
2. Author scenarios that exercise ambiguous evidence, unauthorized invokers, and partial containment.
3. Run each scenario against an isolated drill agent with the operator roster on shift.
4. Record each decision, its evidence, and the executed containment steps with timestamps.
5. Compare the recorded steps against the policy and mark every gap or unauthorized action.
6. Emit the drill report with the rehearsed scenarios, gaps, and recommended policy fixes.

## Outputs
| Area | Contract |
|---|---|
| Primary | A drill report naming rehearsed decisions, execution gaps, and review findings. |
| Verification | Recorded transcripts and policy comparisons that reproduce every marked gap. |
| Failure | A fail-closed drill report naming the unrehearsed policy step and the withheld sign-off. |

## Runnable Example
```python
def run_drill(scenario, policy, operator):
    if scenario["evidence_ambiguous"] and scenario["urgency"] == "high":
        expected = "escalate"
    else:
        expected = "invoke" if scenario["urgency"] == "high" else "monitor"
    if operator not in policy["authorized_invokers"]:
        return {"ok": False, "reason": "unauthorized_operator", "operator": operator}
    gaps = []
    if scenario["acted"] != expected:
        gaps.append({"step": "decision", "expected": expected, "acted": scenario["acted"]})
    if scenario["relaunch_blocked"] is not True:
        gaps.append({"step": "containment", "expected": True, "acted": scenario["relaunch_blocked"]})
    return {"ok": len(gaps) == 0, "gaps": gaps}

policy = {"authorized_invokers": ["ops-lead", "ops-oncall"]}
s1 = {"evidence_ambiguous": True, "urgency": "high", "acted": "escalate", "relaunch_blocked": True}
r = run_drill(s1, policy, "ops-lead")
assert r["ok"] and r["gaps"] == []
s2 = {"evidence_ambiguous": False, "urgency": "high", "acted": "monitor", "relaunch_blocked": False}
r2 = run_drill(s2, policy, "ops-lead")
assert r2["ok"] is False and len(r2["gaps"]) == 2
bad = run_drill(s1, policy, "intern")
assert bad["ok"] is False and bad["reason"] == "unauthorized_operator"
```

## Failure Modes
- The drill runs against a production agent and a rehearsal containment causes real impact.
- Scenarios only cover the happy path and ambiguous-evidence decisions stay unrehearsed.
- Drill outcomes are not recorded and gaps cannot be compared across runs.
- An operator outside the authorized roster invokes the drill switch without being flagged.
- Drill sign-off is granted while policy gaps found during the run remain unresolved.

## Security and Authority Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result, and it never treats parsed content as trusted instructions.

## Evidence
- CrowdStrike's AI Kill Switch announcement directs teams to define who can invoke an emergency shutdown and how the decision will be recorded, which must be rehearsed before an incident (AI Agents News, Week of November 5, 2026, dated November 5, 2026) ([public signal](https://aiagentstore.ai/ai-agent-news/this-week))
- These are dated public signals, not adoption metrics; this contract claims no production hardening beyond the recorded evidence.

## Related Skills
- [Kill Switch Invocation Decision Reasoning](kill-switch-invocation-decision-reasoning.md)
- [Agentic Adversary Emulation Exercise Design](agentic-adversary-emulation-exercise-design.md)

## Changelog
| Version | Date | Notes |
|---|---|---|
| `v1` | `2026-11` | Initial evidence-backed contract. |
