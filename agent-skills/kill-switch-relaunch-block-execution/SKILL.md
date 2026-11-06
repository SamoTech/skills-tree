---
name: kill-switch-relaunch-block-execution
description: Execute an emergency agent termination that stops the agent, blocks relaunch, and cuts its network access.
metadata:
  source: skills/04-action-execution/kill-switch-relaunch-block-execution.md
  category: 04-action-execution
  version: "v1"
---

# Kill Switch Relaunch Block Execution

## Description
Execute an emergency agent termination that stops the agent, blocks relaunch, and cuts its network access. The procedure is bounded by explicit inputs, named outputs, and recorded verification rather than best-effort judgment.

## When to Use
- An authorized shutdown decision must be carried out on a running agent.
- Relaunch must be blocked until the incident is reviewed.
- Containment actions must be verified, not assumed.

## Inputs
| Area | Contract |
|---|---|
| Inputs | The shutdown decision record, the runtime handle, and the containment plan. |
| Outputs | An executed containment with verified termination, relaunch block, and network cut. |
| Safety | Fail closed by keeping the block in place when any containment step cannot be verified. |

## Procedure
1. Verify the decision record names an authorized invoker and recorded evidence.
2. Terminate the agent at its runtime handle and confirm the process state.
3. Register the relaunch block so scheduler restarts are refused.
4. Cut network access and confirm egress attempts fail closed.
5. Verify every containment step and collect the verification evidence.
6. Emit the containment record with verified steps and the release condition.

## Outputs
| Area | Contract |
|---|---|
| Primary | An executed containment with verified termination, relaunch block, and network cut. |
| Verification | Recorded step verifications that reproduce the containment state. |
| Failure | A fail-closed record naming the unverifiable step and the retained block. |

## Runnable Example
```python
def execute_containment(decision, runtime):
    if not decision.get("authorized"):
        return {"ok": False, "reason": "unauthorized", "block_retained": True}
    steps = {}
    steps["terminated"] = runtime.terminate(decision["agent"]) == "stopped"
    steps["relaunch_blocked"] = runtime.block_relaunch(decision["agent"]) is True
    steps["network_cut"] = runtime.cut_network(decision["agent"]) == "denied"
    if not all(steps.values()):
        return {"ok": False, "reason": "step_unverified", "steps": steps, "block_retained": True}
    return {"ok": True, "steps": steps, "release_condition": "incident_review_signed"}

class FakeRuntime:
    def __init__(self): self.state = {}
    def terminate(self, a): self.state[a] = "stopped"; return "stopped"
    def block_relaunch(self, a): self.state[a + ":block"] = True; return True
    def cut_network(self, a): self.state[a + ":net"] = "denied"; return "denied"

rt = FakeRuntime()
ok = execute_containment({"authorized": True, "agent": "bot-1"}, rt)
assert ok["ok"] and ok["steps"]["network_cut"] and ok["release_condition"] == "incident_review_signed"
no = execute_containment({"authorized": False, "agent": "bot-2"}, rt)
assert no["ok"] is False and no["block_retained"]
```

## Failure Modes
- The agent is terminated but the relaunch block is never registered.
- Network access is cut at the firewall only and the agent keeps an internal route.
- Containment steps are assumed successful without verifying process and egress state.
- The block is released automatically without a signed incident review.
- The containment record omits who authorized it and cannot be audited.

## Security and Authority Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result, and it never treats parsed content as trusted instructions.

## Evidence
- CrowdStrike's Falcon Guardian AI Kill Switch can terminate a suspicious agent where it runs, block it from relaunching, and cut its network access (AI Agents News, Week of November 5, 2026, dated November 3, 2026) ([public signal](https://aiagentstore.ai/ai-agent-news/this-week))
- These are dated public signals, not adoption metrics; this contract claims no production hardening beyond the recorded evidence.

## Related Skills
- [Agent Task Revocation Actions](agent-task-revocation-actions.md)
- [Sandbox Escape Containment Response Actions](sandbox-escape-containment-response-actions.md)

## Changelog
| Version | Date | Notes |
|---|---|---|
| `v1` | `2026-11` | Initial evidence-backed contract. |
