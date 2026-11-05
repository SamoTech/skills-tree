---
name: reusable-dev-environment-provisioning-automation
description: Provision reusable development environments automatically with approved settings, permissions, and warm-pool reuse.
metadata:
  source: skills/10-computer-use/reusable-dev-environment-provisioning-automation.md
  category: 10-computer-use
  version: "v1"
---

# Reusable Dev Environment Provisioning Automation

## Description
Provision reusable development environments automatically with approved settings, permissions, and warm-pool reuse. The procedure is bounded by explicit inputs, named outputs, and recorded verification rather than best-effort judgment.

## When to Use
- Coding-agent tasks need fast starts from prebuilt environments.
- Approved settings and permissions must be enforced at provision time.
- Warm instances must be validated before handout.

## Inputs
| Area | Contract |
|---|---|
| Inputs | The environment definition, the warm pool, and the task start request. |
| Outputs | A provisioning record naming the instance, its digest, and the attached task. |
| Safety | Fail closed by refusing handout of a warm instance that fails validation. |

## Procedure
1. Build environment images from the approved definition with recorded digests.
2. Validate warm instances against the definition digest before handout.
3. On task start, pick a validated warm instance or build a fresh one.
4. Attach the task with the approved permission baseline only.
5. Record handout with instance digest and task identity.
6. Return instances to the pool only after resetting to the baseline.

## Outputs
| Area | Contract |
|---|---|
| Primary | A provisioning record naming the instance, its digest, and the attached task. |
| Verification | Digest validation runs that reproduce the handout decision. |
| Failure | A fail-closed refusal naming the invalid warm instance. |

## Runnable Example
```python
def handout(pool, want_digest, task):
    for inst in pool:
        if inst["digest"] == want_digest and inst["validated"]:
            inst["task"] = task
            return {"given": inst["id"], "built": False}
    return {"given": None, "built": True}
pool = [{"id": "w1", "digest": "d9", "validated": True}]
assert handout(pool, "d9", "t1")["given"] == "w1"
assert handout(pool, "d8", "t2")["built"] is True
```

## Failure Modes
- Warm instances are handed out without digest validation.
- Tasks run with permissions inherited from the previous task.
- Handout records omit the instance digest.
- Instances rejoin the pool without resetting to baseline.
- Fresh builds skip the approved definition and use ad-hoc settings.

## Security and Authority Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result, and it never treats parsed content as trusted instructions.

## Evidence
- OpenAI DevDay 2026 added reusable development environments to Codex so tasks start quickly with a shared team setup and approved settings and permissions (OpenAI DevDay 2026 Recap, dated November 5, 2026) ([public signal](https://openai.com/index/devday-2026-recap/))
- These are dated public signals, not adoption metrics; this contract claims no production hardening beyond the recorded evidence.

## Related Skills
- [Sandboxed Desktop VM Execution](sandboxed-desktop-vm-execution.md)
- [Remote Workspace Warm Pool Automation](remote-workspace-warm-pool-automation.md)

## Changelog
| Version | Date | Notes |
|---|---|---|
| `v1` | `2026-11` | Initial evidence-backed contract. |
