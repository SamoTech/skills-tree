---
name: memory-redaction
description: Remove secrets and personal data from memory before persistence or sharing, verify removal with a second pass, and record what was redacted rather than deleting silently.
metadata:
  source: skills/03-memory/memory-redaction.md
  category: 03-memory
  version: "v1"
---

# Memory Redaction

## Description
Remove secrets and personal data from memory before persistence or sharing, verify removal with a second pass, and record what was redacted rather than deleting silently. The procedure is constrained by explicit inputs and acceptance criteria rather than best-effort judgment alone.

## When to Use
- memory content contains secrets or personal data before it is stored or shared before downstream steps can proceed safely.
- Ambiguity or missing evidence would change the outcome.
- The result must be recorded with reasons and evidence for later verification.

## Inputs / Outputs
| Area | Contract |
|---|---|
| Inputs | Task context, candidate inputs, and explicit acceptance criteria for memory redaction work. |
| Outputs | A decision or artifact with recorded reasons, rejected alternatives, and verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Define the goal, the constraints, and the boundary of what this procedure may change.
2. Inventory the available inputs and flag gaps or ambiguities that block progress.
3. Execute the memory redaction steps in a bounded, checkpointed way.
4. Compare the actual outcome against the expected outcome and record deviations.
5. On failure, apply the declared fallback path, and never widen permissions to recover.
6. Emit a structured result with evidence and provenance for downstream consumers.

## Runnable Example
```python
import re

def redact(text):
    return re.sub(r"(?i)(api[_-]?key|token|password)\s*[=:]\s*\S+", r"\1=<redacted>", text)

def verify_clean(text):
    return "<redacted>" in text or not re.search(r"(?i)(api[_-]?key|token|password)\s*[=:]\s*\S+", text)

out = redact("api_key=sk-12345 endpoint=v1")
assert "sk-12345" not in out and verify_clean(out)
assert verify_clean("nothing sensitive here")
```

## Failure Modes
- Redacting one pass with no verification.
- Deleting context the agent still needs to complete the task.
- Redacting logs but not the memory store.
- Missing secrets in non-obvious encodings.
- No record of what was redacted and why.

## Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result.

## Evidence
Secret and PII handling in agent memory is a recurring 2026 compliance topic in public coverage; this is a dated signal, not an adoption metric.

## Related
- redacted-content-detection.md
- memory-quality-auditing.md
- retention-policy.md
