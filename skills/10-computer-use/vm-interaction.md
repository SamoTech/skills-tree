---
title: "Vm Interaction"
category: 10-computer-use
level: advanced
stability: stable
version: v2
description: "Interact with a verified virtual-machine display using bounded input actions and explicit VM identity."
added: "2025-03"
related: [sandboxed-desktop-vm-execution, vm-sandbox-action-audit-automation]
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-10-computer-use-vm-interaction.json)

# Vm Interaction

**Category:** `computer-use`
**Skill Level:** `advanced`
**Stability:** `stable`
**Added:** 2025-03

### Description

Interact with a verified virtual-machine display using bounded input actions and explicit VM identity. The VM boundary is the isolation boundary: verify which VM is receiving input, act inside the declared bounds, and record actions for audit because the VM is the blast-radius container.

### Inputs / Outputs

| Direction | Field | Type | Contract |
|---|---|---|---|
| Input | vm | object | The explicit VM identity (instance, snapshot state) receiving input |
| Input | action | object | The bounded input action (click, type, key) in guest coordinates |
| Output | state | object | The observed guest state after the action |
| Output | check | object | Verified postcondition and audit record reference |

### Procedure
1. Verify the VM identity and that the guest is at an interactable state (logged in, not paused).
2. Resolve guest coordinate space and scaling (host pointer mapping, guest resolution).
3. Perform the bounded input action and capture the resulting guest state.
4. Verify the expected guest postcondition before the next action.
5. Record the action for audit; on failure, restore the declared snapshot rather than improvising.

### Example

```python
vm = {"id": "sandbox-vm-12", "state": "running", "guest_res": {"w": 1920, "h": 1080}}
assert vm["state"] == "running", "interact only with a running, interactable guest"
action = {"kind": "click", "guest_point": {"x": 960, "y": 540}}
in_bounds = 0 <= action["guest_point"]["x"] < vm["guest_res"]["w"]
assert in_bounds, "action outside guest bounds"
audit = {"actions": 1, "recorded": True}
assert audit["recorded"], "guest actions must be recorded for audit"
print({"vm": vm["id"], "acted": action["kind"], "audit_recorded": True})
```

### Related Skills

- [Sandboxed Desktop Vm Execution](sandboxed-desktop-vm-execution.md) - the sandbox lifecycle
- [Vm Sandbox Action Audit Automation](vm-sandbox-action-audit-automation.md) - audit the recorded actions
- [Approval Before Destructive Tools](../14-security/approval-before-destructive-tools.md) - gate destructive guest actions

## Failure Modes

- The guest is paused, locked, or mid-boot and inputs go nowhere or into a lock screen.
- Host-to-guest pointer scaling maps actions to the wrong guest coordinates.
- Host keyboard shortcuts are captured by the guest (or vice versa) and trigger unintended actions.
- A snapshot rollback silently discards state the workflow assumed persisted.
- Shared folders or clipboard create unintended side channels out of the VM.

## Changelog
- v2 (2026-11): Structural modernization; added the input/output contract table, a deterministic example, an execution procedure, and corpus-verified related links (replaced the non-corpus input-guardrails/output-guardrails/self-category pointers).
- v1 (2025-03): Initial entry.

## Evidence

- https://agentskills.io/specification

Evidence status: implementation guidance only; no benchmark claim is made without reproducible evidence.
