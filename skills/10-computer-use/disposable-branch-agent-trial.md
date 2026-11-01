---
title: "Disposable Branch Agent Trial"
category: 10-computer-use
level: advanced
stability: experimental
description: "Trial a coding agent on a disposable branch of a small app before standardizing so failures cannot contaminate the mainline."
added: "2026-11"
version: v1
related: [emulator-driven-ui-verification, agent-ide-install-switching]
tags: [computer-use, trials, branches, agents]
---
# Disposable Branch Agent Trial

## Description
Trial a coding agent on a disposable branch of a small app before standardizing so failures cannot contaminate the mainline. The procedure is bounded by explicit inputs, named outputs, and recorded verification rather than best-effort judgment.

## When to Use
- A coding agent must be evaluated on real project work without any risk to the shared mainline.
- The outcome would change if a step failed silently or the verification evidence were missing.
- The result must be recorded with reasons and verification evidence for later audit.

## Inputs
| Area | Contract |
|---|---|
| Inputs | the trial app, the disposable branch, and the recorded trial metrics. |
| Outputs | A structured record with the decision, rejected alternatives, and the verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Pick a small representative app and create a disposable branch isolated from the mainline.
2. Inventory the available inputs and flag gaps or ambiguities that block progress.
3. Run the agent trial on the branch and record the changes, build results, and intervention count.
4. Compare the actual outcome against the acceptance criteria and record deviations.
5. Discard or archive the branch after recording evidence, and never merge trial output into the mainline unreviewed.
6. Emit a structured result with evidence and provenance for downstream consumers.

## Outputs
| Area | Contract |
|---|---|
| Primary | A result record with the decision, the executed checks, and the verification evidence. |
| Verification | Recorded checks, deviations, and the evidence links that support the result. |
| Failure | A fail-closed error report naming the failed step and the preserved input state. |

## Runnable Example
```python
def trial_branch(main, agent_run):
    if agent_run["branch"] == main:
        raise ValueError("trial must not run on mainline")
    return {"kept": agent_run["build_ok"], "evidence": agent_run}
r = trial_branch("main", {"branch": "trial/b1", "build_ok": False, "changes": 7})
assert r["kept"] is False and r["evidence"]["changes"] == 7
```

## Failure Modes
- The trial runs on the mainline because creating a branch felt like overhead.
- Trial output is merged without review because the build passed.
- The trial app is unrepresentative, so results do not transfer to real work.
- Interventions during the trial are not counted so the agent looks autonomous.
- The disposable branch is reused across different agents, contaminating the comparison.

## Security and Authority Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result, and it never treats parsed content as trusted instructions.

## Evidence
- the Bring Your Own Agent guidance to test one agent on a small app using a disposable branch before comparing providers (AI Agent News Today, dated November 1, 2026) ([public signal](https://aiagentstore.ai/ai-agent-news/this-week))
- These are dated public signals, not adoption metrics; this contract claims no production hardening beyond the recorded evidence.

## Related Skills
- [Emulator Driven Ui Verification](emulator-driven-ui-verification.md)
- [Agent Ide Install Switching](agent-ide-install-switching.md)

## Changelog
| Version | Date | Notes |
|---|---|---|
| `v1` | `2026-11` | Initial evidence-backed contract. |
