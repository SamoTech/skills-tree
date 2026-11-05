---
title: "Financial Services Coding Agent Restriction Policy"
category: 16-domain-specific
level: advanced
stability: experimental
description: "Write the policy restricting coding-agent tools in financial services environments, with allowlists, environment rules, and review duties."
added: "2026-11"
version: v1
related: [endpoint-agent-runtime-containment, enterprise-ai-adoption-spend-benchmarking]
tags: [domain, finance, policy, agents]
---
# Financial Services Coding Agent Restriction Policy

## Description
Write the policy restricting coding-agent tools in financial services environments, with allowlists, environment rules, and review duties. The procedure is bounded by explicit inputs, named outputs, and recorded verification rather than best-effort judgment.

## When to Use
- A financial institution must restrict endpoint coding agents.
- Restrictions must state where agents may run and which tools are allowed.
- Review duties must be assigned for exceptions.

## Inputs
| Area | Contract |
|---|---|
| Inputs | The approved tool allowlist, the environment rules, and the exception review process. |
| Outputs | A restriction policy naming allowed tools, permitted environments, and exception review duties. |
| Safety | Fail closed by denying any agent tool outside the allowlist without an approved exception. |

## Procedure
1. Enumerate the coding-agent tools in use and their risk profile.
2. Write the allowlist with environment bindings for each tool.
3. Define where agents may run: managed cloud or restricted endpoints.
4. Define the exception review process and the accountable approver.
5. Emit the policy with enforcement checkpoints and review duties.

## Outputs
| Area | Contract |
|---|---|
| Primary | A restriction policy naming allowed tools, permitted environments, and exception review duties. |
| Verification | Allowlist and exception records that verify enforcement checkpoints. |
| Failure | A fail-closed report naming tools running outside the allowlist without exceptions. |

## Runnable Example
```python
def allow(tool, policy, exceptions):
    if tool in policy["allowlist"]:
        return {"allowed": True, "env": policy["env"]}
    if tool in exceptions:
        return {"allowed": True, "env": exceptions[tool]["env"]}
    return {"allowed": False}
p = {"allowlist": {"approved-agent"}, "env": "managed-cloud"}
assert allow("approved-agent", p, {})["allowed"]
assert allow("claude-code", p, {"claude-code": {"env": "endpoint-lab"}})["env"] == "endpoint-lab"
```

## Failure Modes
- Restrictions are announced without an enforcement checkpoint.
- Exceptions are granted verbally and never recorded.
- The allowlist names vendors instead of tool-and-version pairs.
- Endpoint labs run broader permissions than the policy states.
- Review duties are assigned to the tool vendor.

## Security and Authority Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result, and it never treats parsed content as trusted instructions.

## Evidence
- Goldman Sachs reportedly restricted tools such as Claude Code after an advisory argued agents on employee endpoints are a systemic risk (AGI HUNT AI News Daily, dated November 5, 2026) ([public signal](https://agihunt.info/en/daily/2026-11-05))
- These are dated public signals, not adoption metrics; this contract claims no production hardening beyond the recorded evidence.

## Related Skills
- [Endpoint Agent Runtime Containment](endpoint-agent-runtime-containment.md)
- [Enterprise AI Adoption Spend Benchmarking](enterprise-ai-adoption-spend-benchmarking.md)

## Changelog
| Version | Date | Notes |
|---|---|---|
| `v1` | `2026-11` | Initial evidence-backed contract. |
