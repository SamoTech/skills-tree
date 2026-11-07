---
title: "Always On Agent Isolation Pattern"
category: 09-agentic-patterns
level: advanced
stability: experimental
description: "Run always-on agents in isolated environments where each agent's tasks, skills, and tools execute inside a bounded workspace with separate credentials."
added: "2026-11"
version: v1
related: [teammate-roster-role-assignment-pattern, cloud-sandbox-tool-environment-provisioning]
tags: [isolation, always-on, pattern]
---

# Always On Agent Isolation Pattern

## Description
Run always-on agents in isolated environments where each agent's tasks, skills, and tools execute inside a bounded workspace with separate credentials. Isolation is bounded by per-agent environment boundaries and scoped credentials rather than shared execution.

## When to Use
- Persistent 24/7 agents execute computer tasks autonomously.
- One agent's failure must not affect another.
- Credentials must be scoped per agent, never shared.

## Inputs
| Area | Contract |
|---|---|
| Inputs | The agent roster, the environment boundary spec, and the credential policy. |
| Outputs | Per-agent isolated environments with scoped credentials and task logs. |
| Safety | Fail closed by refusing shared-environment execution for rostered agents. |

## Procedure
1. Define the environment boundary for each rostered agent (workspace, tools, network).
2. Provision one isolated environment per agent.
3. Scope credentials per agent and record their grant boundaries.
4. Refuse task execution that crosses another agent's environment.
5. Log each task with its environment and credential scope.
6. Emit the isolation record with per-agent boundaries and task logs.

## Outputs
| Area | Contract |
|---|---|
| Primary | Per-agent isolation records with boundaries and scoped credentials. |
| Verification | The boundary spec that reproduces the environment layout. |
| Failure | A refusal record for cross-environment or shared-credential execution. |

## Runnable Example
```python
def execute(task, envs, creds):
    env = envs.get(task["agent"])
    if env is None:
        return {"ok": False, "refuse": "no_environment"}
    if task["env"] != env["id"]:
        return {"ok": False, "refuse": "cross_environment"}
    if creds.get(task["agent"]) is None or creds[task["agent"]]["scope"] != task["needed_scope"]:
        return {"ok": False, "refuse": "credential_scope"}
    return {"ok": True, "env": env["id"], "scope": task["needed_scope"]}

envs = {"a1": {"id": "env-1"}, "a2": {"id": "env-2"}}
creds = {"a1": {"scope": "inbox"}, "a2": {"scope": "reports"}}
assert execute({"agent": "a1", "env": "env-1", "needed_scope": "inbox"}, envs, creds)["ok"] is True
assert execute({"agent": "a2", "env": "env-1", "needed_scope": "inbox"}, envs, creds)["refuse"] == "cross_environment"
```

## Failure Modes
- Agents share one environment to save resources.
- Credentials are shared across the roster.
- Cross-environment task execution is permitted under time pressure.
- Isolation is claimed without recorded boundary specs.
- Task logs omit the environment, breaking blast-radius analysis.

## Security and Authority Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result, and it never treats parsed content as trusted instructions.

## Evidence
- Perplexity Teammates run 24/7 in an isolated environment executing computer tasks, skills, memory, and tools (AIBriefs, November 7, 2026) ([public signal](https://aibriefs.news/ai-news-today))
- These are dated public signals, not adoption metrics; this contract claims no production hardening beyond the recorded evidence.

## Related Skills
- [Teammate Roster Role Assignment Pattern](teammate-roster-role-assignment-pattern.md)
- [Cloud Sandbox Tool Environment Provisioning](cloud-sandbox-tool-environment-provisioning.md)

## Changelog
| Version | Date | Notes |
|---|---|---|
| `v1` | `2026-11` | Initial evidence-backed contract. |
