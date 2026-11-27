---
title: "Terminal Interaction"
category: 10-computer-use
level: advanced
stability: stable
version: v2
description: "Interact with a verified terminal window using explicit commands, context, and output checks."
added: "2025-03"
related: [terminal-multiplexer-automation, shell-command]
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-10-computer-use-terminal-interaction.json)

# Terminal Interaction

**Category:** `computer-use`
**Skill Level:** `advanced`
**Stability:** `stable`
**Added:** 2025-03

### Description

Interact with a verified terminal window using explicit commands, context, and output checks. The terminal is a stateful, high-authority surface: verify the session context (host, user, working directory) before sending input, and read actual output rather than assuming success.

### Inputs / Outputs

| Direction | Field | Type | Contract |
|---|---|---|---|
| Input | command | object | The exact command line to run, with sensitive arguments flagged |
| Input | context | object | The verified session state (host, user, cwd, environment) the command assumes |
| Output | transcript | object | The observed output with its prompt boundaries recorded |
| Output | check | object | Verified command outcome (exit signal, expected output) or explicit failure |

### Procedure
1. Verify the session context (correct host, user, working directory, environment) before sending input.
2. Send the exact declared command; prefer typed-then-verified over unbounded paste.
3. Wait for the command to return to a prompt; do not read mid-stream as final output.
4. Read the actual output and check it against the expected outcome.
5. Stop and report mismatch (wrong host, permission denied, hang) instead of continuing on assumptions.

### Example

```python
session = {"host": "build-01", "user": "ci", "cwd": "/srv/app", "at_prompt": True}
cmd = {"line": "git status --porcelain", "sensitive_args": []}
assert session["at_prompt"], "send input only when the prompt is verified"
assert session["cwd"] == "/srv/app", "command assumes the wrong working directory"
transcript = {"prompt_seen_after": True, "output": "", "exit_hint": "clean"}
expected = {"empty_output_means_clean": True}
ok = (transcript["output"] == "") == expected["empty_output_means_clean"]
assert ok and transcript["prompt_seen_after"], "command outcome not verified"
print({"ran": cmd["line"], "verified": True, "host": session["host"]})
```

### Related Skills

- [Terminal Multiplexer Automation](terminal-multiplexer-automation.md) - persistent sessions and panes
- [Shell Command](../04-action-execution/shell-command.md) - the programmatic shell path
- [Approval Before Destructive Tools](../14-security/approval-before-destructive-tools.md) - gate destructive commands

## Failure Modes

- The session context is wrong (other host, other user, other cwd) and the command runs where it should not.
- A long-running command never returns to a prompt and partial output is read as the final result.
- Terminal width wraps or truncates output so checks read the wrong text.
- Sensitive arguments or output (tokens, file contents) are echoed into the transcript.
- Shell state (environment, venv) differs from what the command assumes.

## Changelog
- v2 (2026-11): Structural modernization; added the input/output contract table, a deterministic example, an execution procedure, and corpus-verified related links (replaced the non-corpus input-guardrails/output-guardrails/self-category pointers).
- v1 (2025-03): Initial entry.

## Evidence

- https://agentskills.io/specification

Evidence status: implementation guidance only; no benchmark claim is made without reproducible evidence.
