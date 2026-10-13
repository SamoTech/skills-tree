---
name: browser-extension-interaction
description: Automate flows that depend on browser extensions with extension-state verification, permission checks, and fallback when an extension is absent.
metadata:
  source: skills/11-web/browser-extension-interaction.md
  category: 11-web
  version: "v1"
---

# Browser Extension Interaction

## Description
Automate flows that depend on browser extensions with extension-state verification, permission checks, and fallback when an extension is absent. The procedure is constrained by explicit inputs and acceptance criteria rather than best-effort judgment alone.

## When to Use
- a flow only works when a specific extension is present and enabled.
- Ambiguity or missing evidence would change the outcome.
- The result must be recorded with reasons and evidence for later verification.

## Inputs / Outputs
| Area | Contract |
|---|---|
| Inputs | Task context, candidate inputs, and explicit acceptance criteria for browser extension interaction work. |
| Outputs | A decision or artifact with recorded reasons, rejected alternatives, and verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Define the goal, the constraints, and the boundary of what this procedure may change.
2. Inventory the available inputs and flag gaps or ambiguities that block progress.
3. Execute the browser extension interaction steps in a bounded, checkpointed way.
4. Compare the actual outcome against the expected outcome and record deviations.
5. On failure, apply the declared fallback path, and never widen permissions to recover.
6. Emit a structured result with evidence and provenance for downstream consumers.

## Runnable Example
```python
def extension_ready(installed, required):
    missing = [e for e in required if e not in installed]
    return (not missing), missing

ok, missing = extension_ready(['wallet', 'pdf'], ['wallet', 'proxy'])
assert not ok and missing == ['proxy']
```

## Failure Modes
- Assuming the extension is installed because it usually is.
- Ignoring extension version differences in behavior.
- No fallback when a required extension is disabled.
- Driving an extension UI without verifying its state machine.
- Skipping permission checks the extension itself requires.

## Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result.

## Evidence
Extension-dependent automation with fallback appears in 2026 browser-agent requests; this is a dated signal, not an adoption metric.

## Related
- shadow-dom-interaction.md
- js-execution.md
- browser-profile-management.md
