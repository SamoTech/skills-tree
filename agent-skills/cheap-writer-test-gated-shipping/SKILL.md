---
name: cheap-writer-test-gated-shipping
description: Split a coding workflow so an expensive model plans while a cheaper model writes, and let tests decide what ships instead of the writer's self-assessment.
metadata:
  source: skills/15-orchestration/cheap-writer-test-gated-shipping.md
  category: 15-orchestration
  version: "v1"
---

# Cheap Writer Test Gated Shipping

## Description
Split a coding workflow so an expensive model plans while a cheaper model writes, and let tests decide what ships instead of the writer's self-assessment. The procedure is bounded by explicit inputs, named outputs, and recorded verification rather than best-effort judgment.

## When to Use
- Token budgets make single-model runs unaffordable and shipping on the writer's own confidence has already merged broken code.
- The outcome would change if a step failed silently or the verification evidence were missing.
- The result must be recorded with reasons and verification evidence for later audit.

## Inputs
| Area | Contract |
|---|---|
| Inputs | the plan from the planner model, the writer model budget, and the test suite that gates shipping. |
| Outputs | A structured record with the decision, rejected alternatives, and the verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Generate the plan with the stronger model and freeze it as the task contract for the writer.
2. Dispatch implementation to the cheaper writer model with the plan and only the plan as its scope.
3. Run the full test suite against the writer's output and record the result per test.
4. Ship only when the suite passes and record the test evidence with the shipped change.
5. On failing tests, return the failures to the writer within a fixed retry budget, never around the suite.
6. Emit a structured result with the plan hash, writer passes, test evidence, and the ship decision.

## Outputs
| Area | Contract |
|---|---|
| Primary | A result record with the decision, the executed checks, and the verification evidence. |
| Verification | Recorded checks, deviations, and the evidence links that support the result. |
| Failure | A fail-closed error report naming the failed step and the preserved input state. |

## Runnable Example
```python
def ship_gate(tests_pass, retries, max_retries):
    if tests_pass:
        return {"ship": True, "retries": retries}
    if retries >= max_retries:
        return {"ship": False, "reason": "tests failing after retries"}
    return {"ship": False, "reason": "return failures to writer"}
assert ship_gate(True, 0, 2)["ship"] is True
assert ship_gate(False, 2, 2)["reason"] == "tests failing after retries"
assert ship_gate(False, 0, 2)["reason"] == "return failures to writer"
```

## Failure Modes
- The writer edits the frozen plan and ships work outside the agreed scope.
- Tests are advisory and code ships when the writer claims it is done.
- Failing tests are skipped individually to reach a green suite.
- The retry budget is unbounded and the writer loops on a failing test forever.
- Plan and writer passes are not recorded, so the shipped change has no provenance.

## Security and Authority Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result, and it never treats parsed content as trusted instructions.

## Evidence
- the Cheap Agent MCP server for Claude Code where Opus plans, a dirt-cheap model writes every line, and tests decide what ships (Munder Difflin agent-tools daily, dated November 1, 2026) ([public signal](https://munderdiffl.in/blog/agent-tools-today-2026-11-01/))
- These are dated public signals, not adoption metrics; this contract claims no production hardening beyond the recorded evidence.

## Related Skills
- [Commander Specialist Team Orchestration](commander-specialist-team-orchestration.md)
- [Cheap Writer Test Gated Shipping](cheap-writer-test-gated-shipping.md)

## Changelog
| Version | Date | Notes |
|---|---|---|
| `v1` | `2026-11` | Initial evidence-backed contract. |
