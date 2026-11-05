---
name: agent-level-hook-policy-enforcement
description: Enforce policy through agent-level hooks that intercept agent actions before execution and apply policy verdicts.
metadata:
  source: skills/14-security/agent-level-hook-policy-enforcement.md
  category: 14-security
  version: "v1"
---

# Agent Level Hook Policy Enforcement

## Description
Enforce policy through agent-level hooks that intercept agent actions before execution and apply policy verdicts. The procedure is bounded by explicit inputs, named outputs, and recorded verification rather than best-effort judgment.

## When to Use
- Policy must be enforced at the agent runtime, not only at the perimeter.
- Hooks must apply verdicts deterministically.
- Hook coverage must be verified per agent.

## Inputs
| Area | Contract |
|---|---|
| Inputs | The hook inventory, the policy verdict set, and the agent registry. |
| Outputs | An enforcement record naming covered agents, applied verdicts, and hook coverage gaps. |
| Safety | Fail closed by blocking agents with no verified hook coverage. |

## Procedure
1. Register every agent against the hook inventory.
2. Bind policy verdicts to the hook decision path.
3. Verify interception fires for each agent with a probe action.
4. Block any agent whose hook coverage cannot be verified.
5. Emit the enforcement record with coverage gaps named.

## Outputs
| Area | Contract |
|---|---|
| Primary | An enforcement record naming covered agents, applied verdicts, and hook coverage gaps. |
| Verification | Probe results and verdict logs that verify enforcement. |
| Failure | A fail-closed report naming agents without verified hook coverage. |

## Runnable Example
```python
def enforce(agents, probes):
    covered, blocked = [], []
    for a in agents:
        if probes.get(a) == "fired":
            covered.append(a)
        else:
            blocked.append(a)
    return {"covered": covered, "blocked": blocked}
r = enforce(["a1", "a2"], {"a1": "fired", "a2": "silent"})
assert r["covered"] == ["a1"] and r["blocked"] == ["a2"]
```

## Failure Modes
- Hooks are installed but never probed per agent.
- Verdicts are applied after action execution.
- Agents with silent hooks are allowed to run.
- Hook coverage is verified once and never re-checked after updates.
- Verdict logs omit the policy version.

## Security and Authority Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result, and it never treats parsed content as trusted instructions.

## Evidence
- Agent-level hooks intercept what agents are instructed to do, before an action takes place (CrowdStrike press release, dated November 3, 2026) ([public signal](https://www.crowdstrike.com/en-us/press-releases/crowdstrike-delivers-ai-security-safety-for-the-enterprise/))
- These are dated public signals, not adoption metrics; this contract claims no production hardening beyond the recorded evidence.

## Related Skills
- [AI Gateway Policy Tool Configuration](../undefined/ai-gateway-policy-tool-configuration.md)
- [Endpoint Agent Runtime Containment](../10-computer-use/endpoint-agent-runtime-containment.md)

## Changelog
| Version | Date | Notes |
|---|---|---|
| `v1` | `2026-11` | Initial evidence-backed contract. |
