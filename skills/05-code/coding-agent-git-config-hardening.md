---
title: "Coding Agent Git Config Hardening"
category: 05-code
level: advanced
stability: experimental
description: "Audit and constrain git configuration used by coding agents so automated commits cannot be silently redirected through altered settings."
added: "2026-10"
version: v1
related: [git-operations, security-scanning, static-analysis]
tags: [git, security, coding-agents]
---

# Coding Agent Git Config Hardening

## Description
Audit and constrain git configuration used by coding agents so automated commits cannot be silently redirected through altered settings. The procedure is constrained by explicit inputs and acceptance criteria rather than best-effort judgment alone.

## When to Use
- a coding agent commits to git and its configuration must be verified before the commit boundary is crossed.
- Ambiguity or missing evidence would change the outcome.
- The result must be recorded with reasons and evidence for later verification.

## Inputs / Outputs
| Area | Contract |
|---|---|
| Inputs | Task context, candidate inputs, and explicit acceptance criteria for coding agent git config hardening work. |
| Outputs | A decision or artifact with recorded reasons, rejected alternatives, and verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Define the goal, the constraints, and the boundary of what this procedure may change.
2. Inventory the available inputs and flag gaps or ambiguities that block progress.
3. Execute the coding agent git config hardening steps in a bounded, checkpointed way.
4. Compare the actual outcome against the expected outcome and record deviations.
5. On failure, apply the declared fallback path, and never widen permissions to recover.
6. Emit a structured result with evidence and provenance for downstream consumers.

## Runnable Example
```python
def audit_config(cfg, allowed):
    problems = []
    if cfg.get("core.sshCommand") and cfg["core.sshCommand"] != allowed["core.sshCommand"]:
        problems.append("core.sshCommand-overridden")
    if "url.insteadOf" in cfg:
        problems.append("url-rewrite-active")
    return problems or []

base = {"core.sshCommand": "ssh -i /etc/agent/key"}
assert audit_config({"core.sshCommand": "ssh -i /etc/agent/key"}, base) == []
assert audit_config({"core.sshCommand": "ssh -i /tmp/other"}, base) == ["core.sshCommand-overridden"]
```

## Failure Modes
- Committing without checking core.sshCommand or url rewrites first.
- Trusting a repository-local config over the agent-scoped config.
- Leaving agent credentials writable by the repository content.
- Ignoring hook paths that point outside the repository.
- No log of the config state at commit time.

## Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result.

## Evidence
Coding-agent git configuration hijacks were publicly described as an attack path in 2026 agent security coverage; this is a dated public signal, not an adoption metric.

## Related
- git-operations.md
- security-scanning.md
- static-analysis.md
