---
title: "Workflow Versioning"
category: 15-orchestration
level: intermediate
stability: experimental
description: "Version workflow definitions explicitly and record the version in every execution so in-flight runs keep a stable identity while definitions evolve without silent breakage."
added: "2026-10"
version: v1
related: ["multi-agent-run-config", "state-machine"]
---

# Workflow Versioning

Category: Orchestration | Level: intermediate | Stability: experimental | Version: v1

## Description

A workflow definition is code that runs many times. Versioning it explicitly — semantic bumps, a recorded version per execution, and a written rule for what counts as compatible — separates "the run behaved as defined" from "the definition changed underneath the run". Executions carry their definition version, so a result can always be traced to the exact steps that produced it.

## When to Use

Use whenever a multi-step workflow runs repeatedly and its steps, prompts, tool wiring, or output schema may change over time.

Do not use one mutable definition with in-place edits; every execution should be able to name the version that produced it.

## Inputs

| Input | Type | Required | Description |
|---|---|---|---|
| `definition` | `workflow` | Yes | The step graph and its metadata |
| `change_set` | `list[change]` | Yes | The edits being applied to the definition |
| `running_executions` | `list[execution]` | No | Executions still using earlier versions |
| `compatibility_rule` | `map` | Yes | What the project classifies as breaking, additive, or fix |

## Procedure

1. Assign each definition an explicit version; an unversioned definition is a defect, not a default.
2. Classify every change against the written rule: step removal, output schema change, or semantic edits are breaking; additive steps are additive; wording fixes are fixes.
3. Record the definition version inside every execution at start; a result without a version cannot be interpreted later.
4. Pin in-flight executions to the version they started with; migrate only between runs, never during one.
5. For breaking bumps, provide an explicit migration or a compatibility window; never change a version in place.
6. Keep the definition history queryable so any past result can be replayed against its own version.

## Outputs

| Output | Type | Description |
|---|---|---|
| `new_version` | `version` | The bumped version after applying the change set |
| `in_flight_policy` | `pin | migrate` | What happens to executions started under the old version |
| `history_entry` | `map` | Change set, bump class, and timestamp |

## Runnable Example

```python
def bump_version(current, change_class):
    """Bump major, minor, or patch per the change classification."""
    major, minor, patch = (int(part) for part in current.lstrip("v").split("."))
    if change_class == "breaking":
        return f"v{major + 1}.0.0"
    if change_class == "additive":
        return f"v{major}.{minor + 1}.0"
    return f"v{major}.{minor}.{patch + 1}"

print(bump_version("v1.4.2", "breaking"))
print(bump_version("v1.4.2", "additive"))
print(bump_version("v1.4.2", "fix"))
```

## Failure Modes

| Failure Mode | Cause | Mitigation |
|---|---|---|
| In-place mutation | Definition edited while executions reference it | Versions are immutable; changes are new versions |
| Unlabeled executions | Runs that cannot name their definition version | Stamp the version into every execution at start |
| Silent breaking changes | Output schema edited without a major bump | Classify changes against a written rule, not mood |
| Migration drift | In-flight runs partially migrated mid-run | Pin in-flight runs; migrate only between runs |
| Lost history | Old definitions deleted after the switch | Keep every version queryable for replay |

## Security and Authority Boundary

Versioning preserves the structure of orchestration; it does not pin model behavior. Two executions of the same version can still differ from model sampling — output reproducibility needs seed, prompt, and model tracking of its own.

## Evidence

This skill is grounded in dated public implementation references:

1. The Semantic Versioning specification (https://semver.org/).
2. Wikipedia's overview of schema evolution under version changes (https://en.wikipedia.org/wiki/Schema_evolution).

Honest boundary: these are implementation references, not adoption or demand evidence; this entry was added under the owner-directed corpus expansion recorded in `meta/memory/DECISIONS.md`, and no demand signal is claimed for it.

## Related Skills

- [Multi-Agent Run Config](multi-agent-run-config.md) — run configuration that should carry the workflow version it executes.
- [State Machine](state-machine.md) — state machine definitions that need the same versioning discipline.

## Changelog

| Date | Version | Change |
|---|---|---|
| `2026-10` | v1 | Initial entry added under the owner-directed corpus expansion |
