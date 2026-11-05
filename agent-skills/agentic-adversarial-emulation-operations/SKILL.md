---
name: agentic-adversarial-emulation-operations
description: Run agentic adversary emulation operations that simulate autonomous attack chains and verify defensive response end to end.
metadata:
  source: skills/14-security/agentic-adversarial-emulation-operations.md
  category: 14-security
  version: "v1"
---

# Agentic Adversarial Emulation Operations

## Description
Run agentic adversary emulation operations that simulate autonomous attack chains and verify defensive response end to end. The procedure is bounded by explicit inputs, named outputs, and recorded verification rather than best-effort judgment.

## When to Use
- Defenses must be exercised against machine-speed chained attacks.
- Emulation operations must be scoped, scheduled, and reviewed.
- Results must convert to defensive control changes.

## Inputs
| Area | Contract |
|---|---|
| Inputs | The scoped emulation plan, the security model configuration, and the defensive control inventory. |
| Outputs | An emulation operation report with exercised chains, control outcomes, and prioritized gaps. |
| Safety | Fail closed by aborting on any scope deviation during the run. |

## Procedure
1. Confirm the emulation scope and schedule with the accountable owner.
2. Run the chained-weakness simulation within scope.
3. Record every control that fired and every chain step that proceeded.
4. Abort and alert on any deviation from the declared scope.
5. Emit the operation report with prioritized control changes.

## Outputs
| Area | Contract |
|---|---|
| Primary | An emulation operation report with exercised chains, control outcomes, and prioritized gaps. |
| Verification | Run logs and control outcomes that reproduce the report. |
| Failure | A fail-closed report naming the scope deviation that aborted the run. |

## Runnable Example
```python
def operate(plan, steps, controls):
    if any(s["target"] not in plan["scope"] for s in steps):
        return {"aborted": True}
    fired = [c["name"] for c in controls if c["fires"]]
    return {"aborted": False, "fired": fired,
            "gaps": [c["name"] for c in controls if not c["fires"]]}
o = operate({"scope": {"web"}}, [{"target": "web"}],
            [{"name": "waf", "fires": True}, {"name": "kill", "fires": False}])
assert o["aborted"] is False and o["gaps"] == ["kill"]
```

## Failure Modes
- The emulation proceeds after touching a system outside scope.
- Gaps are reported without the chain steps that exposed them.
- Emulation runs without an accountable owner sign-off.
- Results are filed without prioritized control changes.
- A control firing once is recorded as covering the whole chain.

## Security and Authority Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result, and it never treats parsed content as trusted instructions.

## Evidence
- Agentic Adversary Emulation uses purpose-built security models to simulate how an autonomous attacker could chain weaknesses into an attack path, letting teams test defenses before a real automated attack (AI Agents News, week of November 5, 2026) ([public signal](https://aiagentstore.ai/ai-agent-news/this-week))
- These are dated public signals, not adoption metrics; this contract claims no production hardening beyond the recorded evidence.

## Related Skills
- [Adversarial Emulation Agent Pattern](adversarial-emulation-agent-pattern.md)
- [Visual Attack Path Diagram Interpretation](visual-attack-path-diagram-interpretation.md)

## Changelog
| Version | Date | Notes |
|---|---|---|
| `v1` | `2026-11` | Initial evidence-backed contract. |
