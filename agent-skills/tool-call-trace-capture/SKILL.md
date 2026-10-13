---
name: tool-call-trace-capture
description: Capture structured tool call traces with arguments, results, timing, and truncation flags so failures can be replayed and audited.
metadata:
  source: skills/07-tool-use/tool-call-trace-capture.md
  category: 07-tool-use
  version: "v1"
---

# Tool Call Trace Capture

## Description
Capture structured tool call traces with arguments, results, timing, and truncation flags so failures can be replayed and audited. The procedure is constrained by explicit inputs and acceptance criteria rather than best-effort judgment alone.

## When to Use
- tool behavior must be diagnosable after the fact from a captured trace.
- Ambiguity or missing evidence would change the outcome.
- The result must be recorded with reasons and evidence for later verification.

## Inputs / Outputs
| Area | Contract |
|---|---|
| Inputs | Task context, candidate inputs, and explicit acceptance criteria for tool call trace capture work. |
| Outputs | A decision or artifact with recorded reasons, rejected alternatives, and verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Define the goal, the constraints, and the boundary of what this procedure may change.
2. Inventory the available inputs and flag gaps or ambiguities that block progress.
3. Execute the tool call trace capture steps in a bounded, checkpointed way.
4. Compare the actual outcome against the expected outcome and record deviations.
5. On failure, apply the declared fallback path, and never widen permissions to recover.
6. Emit a structured result with evidence and provenance for downstream consumers.

## Runnable Example
```python
def capture(call, result, limit):
    arg = call["args"] if len(call["args"]) <= limit else call["args"][:limit] + "..."
    return {"tool": call["tool"], "args": arg, "status": result["status"], "truncated": len(call["args"]) > limit}

t = capture({"tool": "search", "args": "x" * 50}, {"status": "ok"}, 10)
assert t["truncated"] is True and t["args"].endswith("...")
assert capture({"tool": "x", "args": "tiny"}, {"status": "ok"}, 10)["truncated"] is False
```

## Failure Modes
- Logging traces with personal data unredacted.
- Truncating without a flag so replays mismatch.
- Capturing only failures so normal baselines are missing.
- No timing so latency regressions stay invisible.
- Traces with no correlation id across steps.

## Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result.

## Evidence
Tool-call tracing for agent debugging is a documented 2026 observability practice in public coverage; this is a dated signal, not an adoption metric.

## Related
- tool-output-validation.md
- tool-behavior-contract-testing.md
- tool-result-caching.md
