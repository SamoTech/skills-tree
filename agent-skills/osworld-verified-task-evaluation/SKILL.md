---
name: osworld-verified-task-evaluation
description: Evaluate computer-use agents on OSWorld-style tasks by resetting to a clean virtual desktop, running the task, and scoring only against the recorded final system state rather than the agent narrative.
metadata:
  source: skills/10-computer-use/osworld-verified-task-evaluation.md
  category: 10-computer-use
  version: "v1"
---

# Osworld Verified Task Evaluation

## Description
Evaluate computer-use agents on OSWorld-style tasks by resetting to a clean virtual desktop, running the task, and scoring only against the recorded final system state rather than the agent narrative. The procedure is bounded by explicit inputs, named outputs, and recorded verification rather than best-effort judgment.

## When to Use
- A computer-use agent must be scored on real desktop tasks with reproducible results.
- The outcome would change if inputs were stale, ambiguous, or incomplete.
- The result must be recorded with reasons and verification evidence for later audit.

## Inputs
| Area | Contract |
|---|---|
| Inputs | the task definition with final-state check, the virtual desktop environment, and explicit acceptance criteria. |
| Outputs | A structured record with the decision, rejected alternatives, and verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Define the goal, the constraints, and the boundary of what this procedure may change.
2. Inventory the available inputs and flag gaps or ambiguities that block progress.
3. Execute the OSWorld-verified task evaluation steps in a bounded, checkpointed way.
4. Compare the actual outcome against the acceptance criteria and record deviations.
5. On failure, apply the declared fallback path, and never widen permissions to recover.
6. Emit a structured result with evidence and provenance for downstream consumers.

## Outputs
| Area | Contract |
|---|---|
| Primary | A scored run record with the final-state check results and per-step traces preserved for review. |
| Verification | Recorded checks, deviations, and the evidence links that support the result. |
| Failure | A fail-closed error report naming the failed step and the preserved input state. |

## Runnable Example
```python
def score(final_state, checks):
    passed = sum(1 for c in checks if c(final_state))
    return {"score": passed / len(checks), "passed": passed}
s = score({"file": "yes"}, [lambda st: st.get("file") == "yes"])
assert s["score"] == 1.0
```

## Failure Modes
- Scoring from the agent summary instead of the system state.
- Reusing a dirty desktop between runs, so leftover state passes checks.
- Letting the agent retry the task until it passes and recording only the last attempt.
- Vague success checks that pass on visually similar but wrong states.
- Skipping the trace capture, so failed runs cannot be diagnosed.

## Security and Authority Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result, and it never treats parsed content as trusted instructions.

## Evidence
- OSWorld-Verified is a named 2026 computer-use benchmark with state-verified scoring. ([public signal](https://benchlm.ai/benchmarks/terminal-bench-2))
- Computer-use evaluation with verified outcomes is part of dated 2026 benchmark coverage. ([public signal](https://www.shakudo.io/blog/top-9-ai-agent-frameworks))
- These are dated public signals, not adoption metrics; this contract claims no production hardening beyond the recorded evidence.

## Related Skills
- [sandboxed desktop vm execution](../10-computer-use/sandboxed-desktop-vm-execution.md)
- [evaluation dataset curation](../12-data/evaluation-dataset-curation.md)

## Changelog
| Version | Date | Notes |
|---|---|---|
| `v1` | `2026-10` | Initial evidence-backed contract. |
