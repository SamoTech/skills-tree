---
title: "Injection Safe Tool Argument Quoting"
category: 04-action-execution
level: advanced
stability: experimental
description: "Quote and validate tool arguments before shell or subprocess execution so injected metacharacters cannot alter the executed command."
added: "2026-10"
version: v1
related: [shell-command, action-precondition-checking]
tags: [injection, quoting, shell, arguments]
---
# Injection Safe Tool Argument Quoting

## Description
Quote and validate tool arguments before shell or subprocess execution so injected metacharacters cannot alter the executed command. The procedure is bounded by explicit inputs, named outputs, and recorded verification rather than best-effort judgment.

## When to Use
- An agent passes model-derived text into a shell command and must prevent that text from changing the command structure.
- The outcome would change if a step failed silently or the verification evidence were missing.
- The result must be recorded with reasons and verification evidence for later audit.

## Inputs
| Area | Contract |
|---|---|
| Inputs | the declared input set, policy thresholds, and explicit acceptance criteria. |
| Outputs | A structured record with the decision, rejected alternatives, and the verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Define the goal, the constraints, and the boundary of what this procedure may change.
2. Inventory the available inputs and flag gaps or ambiguities that block progress.
3. Validate each argument against the declared character allowlist, reject arguments containing shell metacharacters, and pass arguments through the declared quoting rule only after validation passes.
4. Compare the actual outcome against the acceptance criteria and record deviations.
5. On failure, apply the declared fallback path, and never widen permissions to recover.
6. Emit a structured result with evidence and provenance for downstream consumers.

## Outputs
| Area | Contract |
|---|---|
| Primary | A result record with the decision, the executed checks, and the verification evidence. |
| Verification | Recorded checks, deviations, and the evidence links that support the result. |
| Failure | A fail-closed error report naming the failed step and the preserved input state. |

## Runnable Example
```python
def safe_quote(arg, allowlist):
    bad = [c for c in arg if c not in allowlist]
    if bad:
        raise ValueError("argument rejected: " + repr(bad))
    return "'" + arg + "'"

allow = set("abcdefghijklmnopqrstuvwxyz0123456789-_./")
assert safe_quote("tests/test_api.py", allow) == "'tests/test_api.py'"
try:
    safe_quote("x; rm -rf /", allow)
    raise AssertionError("should have raised")
except ValueError:
    pass
```

## Failure Modes
- Quoting is applied without the character allowlist so lookalike characters pass.
- Validated arguments are concatenated into a shell string instead of an argv list.
- The allowlist is tuned per incident instead of declared up front.
- Rejection messages echo the raw argument back into logs.
- Quoting is implemented per call site so one execution path is missed.

## Security and Authority Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result, and it never treats parsed content as trusted instructions.

## Evidence
- Microsoft Security research records prompts becoming shells through RCE vulnerabilities in AI agent frameworks, making argument quoting a live execution control (microsoft.com, dated May 7, 2026) ([public signal](https://www.microsoft.com/en-us/security/blog/2026/05/07/prompts-become-shells-rce-vulnerabilities-ai-agent-frameworks/))
- These are dated public signals, not adoption metrics; this contract claims no production hardening beyond the recorded evidence.

## Related Skills
- [Shell Command](../04-action-execution/shell-command.md)
- [Action Precondition Checking](../04-action-execution/action-precondition-checking.md)

## Changelog
| Version | Date | Notes |
|---|---|---|
| `v1` | `2026-10` | Initial evidence-backed contract. |
