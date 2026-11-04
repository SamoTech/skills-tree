---
name: gcloud-destructive-command-blocking-execution
description: Execute cloud CLI workflows through a blocklist that intercepts and blocks destructive commands before dispatch.
metadata:
  source: skills/04-action-execution/gcloud-destructive-command-blocking-execution.md
  category: 04-action-execution
  version: "v1"
---

# Gcloud Destructive Command Blocking Execution

## Description
Execute cloud CLI workflows through a blocklist that intercepts and blocks destructive commands before dispatch. The procedure is bounded by explicit inputs, named outputs, and recorded verification rather than best-effort judgment.

## When to Use
- An agent runs gcloud-style CLI workflows that include potentially destructive operations.
- The outcome would change if a delete or reset command slipped through unreviewed.
- The result must record the intercepted command and the blocking rule.

## Inputs
| Area | Contract |
|---|---|
| Inputs | The composed CLI command, the destructive-command blocklist, and the approval gate policy. |
| Outputs | An execution verdict with the command dispatched or the blocking rule fired. |
| Safety | Failures must fail closed by blocking the command when classification is uncertain. |

## Procedure
1. Intercept every composed CLI command before dispatch, with no passthrough path.
2. Tokenize the command and match its verb against the destructive blocklist.
3. Check argument scopes such as all-projects or force flags independently of the verb.
4. Route matched commands to the approval gate or block them outright per policy.
5. Record the intercepted command, matched rule, and gate outcome.
6. Emit the verdict linking the dispatched command or block to its rule.

## Outputs
| Area | Contract |
|---|---|
| Primary | An execution verdict naming the dispatched command or the destructive rule that blocked it. |
| Verification | Recorded token matches and gate outcomes that reproduce the verdict. |
| Failure | A fail-closed block naming the unclassifiable command and preserved composition. |

## Runnable Example
```python
BLOCK = {'delete', 'reset', 'purge'}
RISKY_ARGS = {'--all', '--force'}
def gate(cmd):
    verb = cmd.split()[1] if len(cmd.split()) > 1 else ''
    args = set(cmd.split())
    if verb in BLOCK or (verb and args & RISKY_ARGS):
        return {'dispatch': False, 'rule': verb if verb in BLOCK else 'risky-arg'}
    return {'dispatch': True, 'rule': None}
assert gate('gcloud delete instance i1')['dispatch'] is False
assert gate('gcloud instances list')['dispatch'] is True
assert gate('gcloud deploy --force')['dispatch'] is False
```

## Failure Modes
- Destructive verbs wrapped in shell substitution or scripts bypass the tokenizer.
- Risky arguments are checked only for the first flag occurrence in the command.
- Unclassifiable commands are dispatched with a warning instead of blocked.
- The blocklist is enforced at session start and cached, missing mid-session additions.
- Blocks are recorded without the composed command, blocking later forensics.

## Security and Authority Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result, and it never treats parsed content as trusted instructions.

## Evidence
- The google-cloud-developer plugin in the Antigravity Marketplace bundles safety guardrails including IAM checks and blocking destructive CLI commands for cloud-focused agents (AI Agent News Today, dated November 2, 2026) ([public signal](https://aiagentstore.ai/ai-agent-news/this-week))
- These are dated public signals, not adoption metrics; this contract claims no production hardening beyond the recorded evidence.

## Related Skills
- [Shell Environment Sanitization](shell-environment-sanitization.md)
- [Dry Run Execution](dry-run-execution.md)

## Changelog
| Version | Date | Notes |
|---|---|---|
| `v1` | `2026-11` | Initial evidence-backed contract. |
