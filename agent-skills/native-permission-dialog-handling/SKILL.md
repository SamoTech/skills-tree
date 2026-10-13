---
name: native-permission-dialog-handling
description: Detect and respond to native OS permission prompts during automation with declared per-prompt policies instead of reflexive approval.
metadata:
  source: skills/10-computer-use/native-permission-dialog-handling.md
  category: 10-computer-use
  version: "v1"
---

# Native Permission Dialog Handling

## Description
Detect and respond to native OS permission prompts during automation with declared per-prompt policies instead of reflexive approval. The procedure is constrained by explicit inputs and acceptance criteria rather than best-effort judgment alone.

## When to Use
- automation must pass OS permission prompts without silently widening permissions.
- Ambiguity or missing evidence would change the outcome.
- The result must be recorded with reasons and evidence for later verification.

## Inputs / Outputs
| Area | Contract |
|---|---|
| Inputs | Task context, candidate inputs, and explicit acceptance criteria for native permission dialog handling work. |
| Outputs | A decision or artifact with recorded reasons, rejected alternatives, and verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Define the goal, the constraints, and the boundary of what this procedure may change.
2. Inventory the available inputs and flag gaps or ambiguities that block progress.
3. Execute the native permission dialog handling steps in a bounded, checkpointed way.
4. Compare the actual outcome against the expected outcome and record deviations.
5. On failure, apply the declared fallback path, and never widen permissions to recover.
6. Emit a structured result with evidence and provenance for downstream consumers.

## Runnable Example
```python
POLICY = {'notifications': 'allow', 'microphone': 'ask', 'location': 'deny'}
def respond(prompt):
    return POLICY.get(prompt, 'deny')

assert respond('microphone') == 'ask'
assert respond('camera') == 'deny'
```

## Failure Modes
- Approving every permission prompt by default.
- Hard-coding answers for prompts that differ per OS version.
- Missing a prompt because it appeared on a separate surface.
- Granting permissions the task never needed.
- Not recording which permissions were granted during a run.

## Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result.

## Evidence
OS permission-prompt handling with declared policies recurs in 2026 automation security discussions; this is a dated signal, not an adoption metric.

## Related
- ui-element-waiting.md
- computer-use-error-recovery.md
- screen-ocr.md
