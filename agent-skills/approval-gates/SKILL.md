---
name: approval-gates
description: Pause an agent run at defined checkpoints and route the pending action to a human decision, so consequential steps execute only after an explicit approval.
metadata:
  source: skills/09-agentic-patterns/approval-gates.md
  category: 09-agentic-patterns
  version: "v1"
---

# Approval Gates

Category: Agentic Patterns | Level: intermediate | Stability: experimental | Version: v1

## Description

Autonomy is a budget, not a binary. This skill spends it deliberately: the run defines which action classes are safe to execute directly, which require a human decision before they commit, and what information the human needs to decide. A gate is a structured pause — the agent stops, presents the action and its context, and waits; the decision is recorded with the action it authorized, so the audit trail says who allowed what, not just what ran.

## When to Use

Use for irreversible or consequential actions — payments, deletions, production changes, external commitments — and for action classes whose blast radius exceeds a configured threshold.

Do not gate trivial, reversible steps; an approval process that fires a hundred times a day trains its approvers to click through without reading.

## Inputs

| Input | Type | Required | Description |
|---|---|---|---|
| `action` | `record` | Yes | The pending action awaiting authorization |
| `policy` | `map` | Yes | Which action classes execute directly and which gate |
| `context` | `map` | Yes | What the approver needs to decide — inputs, blast radius, reversibility |

## Procedure

1. Classify actions up front: which execute without a gate, which need a human, and which are refused outright regardless of approval.
2. Define the gate payload before the run starts — action, arguments, predicted effect, and rollback path — so the pause presents a decision, not a mystery.
3. Stop cleanly: the agent suspends at the gate, persists the pending action, and surfaces the decision request to the designated approver.
4. Record the verdict with its provenance — who decided, when, and on what evidence — attached to the action it authorized.
5. Execute the approved action exactly as presented; a modified action re-enters the gate rather than riding an old approval.
6. Feed rejections back into policy: repeated refusals of the same action class mean the classification, not the human, is wrong.

## Outputs

| Output | Type | Description |
|---|---|---|
| `decision` | `record` | Approval or rejection with approver identity and timestamp |
| `gate_log` | `list` | Every gated action, its verdict, and its provenance |

## Runnable Example

```python
POLICY = {
    "read_file": "auto",
    "delete_file": "gate",
    "pay_invoice": "gate",
    "drop_table": "refuse",
}

def route(action_name):
    rule = POLICY.get(action_name, "refuse")
    if rule == "auto":
        return ("executed", None)
    if rule == "gate":
        return ("awaiting approval", "gate")
    return ("refused by policy", None)

for name in ["read_file", "delete_file", "drop_table"]:
    status, held = route(name)
    print(name, "->", status, held or "")
```

## Failure Modes

| Failure Mode | Cause | Mitigation |
|---|---|---|
| Rubber-stamping | Approvals granted faster than they can be read | Gate only what is consequential; keep gates rare |
| Gate sprawl | Everything requires approval and nothing moves | Classify most actions as auto; gate the irreversible |
| Approval reuse | A modified action executed on an old approval | Changed actions re-enter the gate |
| Unattributed verdicts | Nobody can say who authorized a past action | Record approver identity and timestamp with every verdict |
| Silent refusal drift | Actions quietly failing as policy tightens | Feed refusal patterns back into policy review |

## Security and Authority Boundary

The gate record is an authority artifact: approvals must bind to the exact action hash and the identity of the approver, and gate logs deserve the same integrity protection as audit logs — an attacker who can forge either owns the blast radius of the agent.

## Evidence

This skill is grounded in dated public implementation references:

1. The NIST AI Risk Management Framework overview (https://www.nist.gov/itl/ai-risk-management-framework).
2. The arXiv paper on human-in-the-loop agent oversight (https://arxiv.org/abs/2503.13657).

Honest boundary: these are implementation references, not adoption or demand evidence; this entry was added under the owner-directed corpus expansion recorded in `meta/memory/DECISIONS.md`, and no demand signal is claimed for it.

## Related Skills

- [Interruptible Agent Flows](interruptible-agent-flows.md) — the suspension mechanism gates build on.
- [Tool Use Loop](tool-use-loop.md) — the execution loop the gate pauses.

## Changelog

| Date | Version | Change |
|---|---|---|
| `2026-10` | v1 | Initial entry added under the owner-directed corpus expansion |
