---
name: agent-eval-regression-gates
description: Run a fixed evaluation suite on every agent or prompt change and block promotion when pass rates regress against the recorded baseline.
metadata:
  source: skills/09-agentic-patterns/agent-eval-regression-gates.md
  category: 09-agentic-patterns
  version: "v1"
---

# Agent Eval Regression Gates

## Description
Run a fixed evaluation suite on every agent or prompt change and block promotion when pass rates regress against the recorded baseline. The procedure is constrained by explicit inputs and acceptance criteria rather than best-effort judgment alone.

## When to Use
- agent or prompt changes must not reach production without a recorded suite result.
- Ambiguity or missing evidence would change the outcome.
- The result must be recorded with reasons and evidence for later verification.

## Inputs / Outputs
| Area | Contract |
|---|---|
| Inputs | Task context, candidate inputs, and explicit acceptance criteria for agent eval regression gates work. |
| Outputs | A decision or artifact with recorded reasons, rejected alternatives, and verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Define the goal, the constraints, and the boundary of what this procedure may change.
2. Inventory the available inputs and flag gaps or ambiguities that block progress.
3. Execute the agent eval regression gates steps in a bounded, checkpointed way.
4. Compare the actual outcome against the expected outcome and record deviations.
5. On failure, apply the declared fallback path, and never widen permissions to recover.
6. Emit a structured result with evidence and provenance for downstream consumers.

## Runnable Example
```python
def gate(new_score, baseline, suite_id):
    record = {'suite': suite_id, 'baseline': baseline, 'score': new_score}
    return ('promote' if new_score >= baseline else 'block'), record

decision, record = gate(0.82, 0.85, 'suite-v3')
assert decision == 'block' and record['suite'] == 'suite-v3'
```

## Failure Modes
- Promoting a change because it feels better without the suite.
- A suite that always passes because cases are trivial.
- Not freezing the suite version with each run.
- Comparing against a stale baseline from an older stack.
- Ignoring metric movement inside the pass threshold.

## Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result.

## Evidence
CI-for-agents requests in 2026 ask for fixed eval suites gating every prompt or agent change; this is a dated signal, not an adoption metric.

## Related
- agent-regression-testing.md
- prompt-version-control.md
- agent-eval-harness-design.md
