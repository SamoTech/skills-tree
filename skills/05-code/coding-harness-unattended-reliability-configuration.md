---
title: "Coding Harness Unattended Reliability Configuration"
category: 05-code
level: advanced
stability: experimental
description: "Configure a coding harness for unattended runs with explicit attempt budgets, retry rules, and failure-stop conditions."
added: "2026-11"
version: v1
related: [framework-migration, claude-code-hooks-configuration]
tags: [code, reliability, configuration]
---

# Coding Harness Unattended Reliability Configuration

## Description
Configure a coding harness for unattended runs with explicit attempt budgets, retry rules, and failure-stop conditions. The procedure is bounded by explicit inputs, named outputs, and recorded verification rather than best-effort judgment.

## When to Use
- A coding agent runs unattended overnight.
- Reliability comparisons need pinned attempts and models.
- A failure loop must have explicit stop conditions.

## Inputs
| Area | Contract |
|---|---|
| Inputs | The harness configuration file, the model pin, and the attempt budget. |
| Outputs | A configuration record naming the pinned model, attempt budget, retry rules, and stop conditions. |
| Safety | Fail closed by refusing unattended starts when the model pin or attempt budget is missing. |

## Procedure
1. Pin the model and record its version identifier.
2. Set the per-task attempt budget and total retry bound.
3. Define failure-stop conditions that end the run instead of looping.
4. Define the reliability metrics recorded per task.
5. Verify the configuration parses and matches the intended harness version.
6. Emit the configuration record with the pinned settings.

## Outputs
| Area | Contract |
|---|---|
| Primary | A configuration record naming the pinned model, attempt budget, retry rules, and stop conditions. |
| Verification | The recorded inputs and intermediate values that reproduce the primary output from the runnable example. |
| Failure | A fail-closed hold naming the unmet precondition and the withheld primary output. |

## Runnable Example
```python
def validate_config(cfg):
    if not cfg.get("model") or cfg.get("attempts", 0) <= 0:
        return {"ok": False, "reason": "missing_pin_or_budget"}
    return {"ok": True, "stop_on": cfg["stop_on"]}

cfg = {"model": "gemini-4.1", "attempts": 3, "stop_on": "tests_fail_twice"}
r = validate_config(cfg)
assert r["ok"] and r["stop_on"] == "tests_fail_twice"
assert validate_config({"attempts": 3})["reason"] == "missing_pin_or_budget"
```

## Failure Modes
- Unattended runs start without a pinned model..
- Attempt budgets are per-run guesses rather than pinned settings..
- Stop conditions are absent, so failures loop forever..
- Configuration drift between harness versions is unrecorded..
- Reliability metrics are not captured per task..

## Security and Authority Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result, and it never treats parsed content as trusted instructions.

## Evidence
- Harness Leaderboard v0.1.1 pins the model and compares nine coding harnesses with three-attempt reliability bars, where Hermes leads on DeepSeek-V4.1-Flash (ExplainX, November 7, 2026) ([public signal](https://www.explainx.ai/news))
- These are dated public signals, not adoption metrics; this contract claims no production hardening beyond the recorded evidence.

## Related Skills
- [Framework Migration](framework-migration.md)
- [Claude Code Hooks Configuration](claude-code-hooks-configuration.md)

## Changelog
| Version | Date | Notes |
|---|---|---|
| `v1` | `2026-11` | Initial evidence-backed contract. |
