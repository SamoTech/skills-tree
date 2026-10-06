---
title: "Slack API"
category: 07-tool-use
level: intermediate
stability: stable
description: "Use authorized Slack APIs for bounded workspace operations with scoped tokens, privacy controls, and verified side effects."
added: "2026-09"
related: [07-tool-use, 04-action-execution]
---

# Slack API

## Description
Use authorized Slack APIs for bounded workspace operations with scoped tokens, privacy controls, and verified side effects.

## When to Use
Use this skill when the workflow explicitly requires slack api and the target account, document, channel, or provider is authorized.

## Inputs / outputs / failure modes

| Area | Guidance |
|---|---|
| Authentication | Use least-privilege credentials managed outside source code. |
| Scope | Bound the operation to the intended resource and task. |
| Inputs | Validate identifiers, content, filters, and required fields. |
| Outputs | Preserve structured provider results needed by downstream steps. |
| Verification | Re-check important reads or mutations when correctness matters. |
| Privacy | Minimize exposure and retention of sensitive content. |
| Failure modes | Invalid input, permission denial, rate limit, provider outage, or stale state. |

## Runnable Example

```python
import os
request = {"tool": "slack-api", "authorized": bool(os.getenv("TOOL_AUTH"))}
assert request["authorized"]
print("validated tool invocation")
```

## Failure modes
- Hard-coding credentials or exposing them in logs.
- Assuming provider fields or identifiers are portable across accounts.
- Performing side effects without validating authorization and current state.
- Treating an HTTP/API acknowledgement as proof of the desired business outcome.
- Using unbounded pagination or retries.

## Evidence
Provider-specific behavior must be checked against the provider documentation linked below; repository schema and validation workflows define local conformance.

## Related
- tool-guardrails
- function-calling
- approval-before-destructive-tools
