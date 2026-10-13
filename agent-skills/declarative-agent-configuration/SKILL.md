---
name: declarative-agent-configuration
description: Define agent behavior in declarative configuration files with schema validation, and refuse to start the agent when the configuration cannot be validated.
metadata:
  source: skills/05-code/declarative-agent-configuration.md
  category: 05-code
  version: "v1"
---

# Declarative Agent Configuration

## Description
Define agent behavior in declarative configuration files with schema validation, and refuse to start the agent when the configuration cannot be validated. The procedure is constrained by explicit inputs and acceptance criteria rather than best-effort judgment alone.

## When to Use
- an agent must be configured from a validated file so behavior is reproducible across runs before downstream steps can proceed safely.
- Ambiguity or missing evidence would change the outcome.
- The result must be recorded with reasons and evidence for later verification.

## Inputs / Outputs
| Area | Contract |
|---|---|
| Inputs | Task context, candidate inputs, and explicit acceptance criteria for declarative agent configuration work. |
| Outputs | A decision or artifact with recorded reasons, rejected alternatives, and verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Define the goal, the constraints, and the boundary of what this procedure may change.
2. Inventory the available inputs and flag gaps or ambiguities that block progress.
3. Execute the declarative agent configuration steps in a bounded, checkpointed way.
4. Compare the actual outcome against the expected outcome and record deviations.
5. On failure, apply the declared fallback path, and never widen permissions to recover.
6. Emit a structured result with evidence and provenance for downstream consumers.

## Runnable Example
```python
def validate(cfg):
    missing = [k for k in ("role", "tools", "limits") if k not in cfg]
    if missing:
        return "reject:" + ",".join(missing)
    if cfg["limits"]["turns"] <= 0:
        return "reject:turns"
    return "ok"

assert validate({"role": "r", "tools": ["search"], "limits": {"turns": 3}}) == "ok"
assert validate({"tools": [], "limits": {"turns": 3}}).startswith("reject")
```

## Failure Modes
- Validating configuration only after the agent has already started.
- Allowing undeclared keys to silently change behavior.
- Storing credentials inline in the configuration file.
- No recorded diff when configuration changes between runs.
- Falling back to defaults when validation fails instead of stopping.

## Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result.

## Evidence
Declarative agent configuration is a 2026 framework theme across public releases of agentic stacks; this is a dated public signal, not an adoption metric.

## Related
- cicd-generation.md
- api-client-generation.md
- requirement-tracing.md
