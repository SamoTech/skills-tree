---
title: "Runbook-Driven Orchestration"
category: 15-orchestration
level: intermediate
stability: experimental
description: "Execute operational workflows as versioned, machine-readable runbooks with declared steps, verification gates, and escalation paths, so automation follows the reviewed procedure exactly."
added: "2026-10"
version: v1
related: ["state-machine","execution-handoff"]
---

# Runbook-Driven Orchestration

Category: Orchestration | Level: intermediate | Stability: experimental | Version: v1

## Description

A runbook-driven run follows the document, not the model’s improvisation. The skill covers expressing an operational procedure as a versioned runbook with explicit steps, preconditions, verification commands, and escalation paths; validating the runbook before use; executing steps with state recorded at each gate; and stopping on any failed verification instead of continuing creatively. The run remains auditable because the automation’s actions map one-to-one onto reviewed instructions.

## When to Use

Use for operational procedures that must be executed consistently across shifts and operators: deployments, incident mitigation, and routine maintenance with failure risk.

Do not let the executor improvise around a failed step. A failed verification stops the run and escalates; creative continuation defeats the point of a reviewed procedure.

## Inputs

| Input | Type | Required | Description |
|---|---|---|---|
| `runbook` | `object` | Yes | Versioned, machine-readable procedure with steps and gates |
| `context` | `object` | Yes | Environment parameters the runbook references |
| `mode` | `enum` | No | `execute` (default) or `dry-run` for rehearsal |

## Procedure

1. Load the runbook version under approval and verify its signature or review status.
2. Validate the runbook: every step has a command, expected outcome, and failure action.
3. Execute steps in order, recording state and output at every gate.
4. Run each verification gate before advancing; a failed gate stops the run.
5. Escalate through the declared path with the recorded state attached, never past it.
6. Archive the run record: runbook version, context, outputs, and every gate result.

## Outputs

| Output | Type | Description |
|---|---|---|
| `run_record` | `table` | Steps executed with outputs and gate results |
| `failed_gate` | `object` | The verification that stopped the run, with evidence |
| `escalation` | `object` | Where the run was handed off and with what state |

## Runnable Example

```python
def execute_runbook(steps, mode="execute"):
    """steps: [(name, gate_ok)] already verified per step"""
    record = []
    for name, gate_ok in steps:
        if not gate_ok:
            return {"status": "halted", "failed_step": name, "record": record}
        record.append({"step": name, "result": "passed"})
    return {"status": "completed", "record": record}

print(execute_runbook([("backup", True), ("migrate", True), ("verify", False)]))
```

## Failure Modes

| Failure Mode | Cause | Mitigation |
|---|---|---|
| Improvised continuation | Executor worked around a failed gate | Hard stop on any failed verification |
| Runbook drift | Documented procedure diverged from reality | Dry-run validation on schedule and before use |
| Missing failure actions | A step fails with no declared response | Require a failure action per step at validation |
| Ambiguous context | Parameters resolved by guesswork mid-run | Bind all context before step one |
| Unreviewed edits | Runbook changed without approval | Version, review, and refuse unapproved versions |

## Security and Authority Boundary

Runbooks encode privileged operations. Sign and review runbook versions, execute with the least privilege the steps require, and record every gate result immutably, because the run record is the audit evidence for what automation did to production.

## Evidence

This skill is grounded in dated public implementation references:

1. The Ansible automation engine for executable operational procedures (https://github.com/ansible/ansible).
2. The Google SRE book’s treatment of runbooks and operational automation (https://sre.google/sre/).

Honest boundary: these are implementation references, not adoption or demand evidence; this entry was added under the owner-directed corpus expansion recorded in `meta/memory/DECISIONS.md`, and no demand signal is claimed for it.

## Related Skills

- [State Machine](state-machine.md) — the step-and-gate structure a runbook encodes.
- [Execution Handoff](execution-handoff.md) — the escalation path a halted run uses.

## Changelog

| Date | Version | Change |
|---|---|---|
| `2026-10` | v1 | Initial entry added under the owner-directed corpus expansion |
