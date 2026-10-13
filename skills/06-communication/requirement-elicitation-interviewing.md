---
title: "Requirement Elicitation Interviewing"
category: 06-communication
level: advanced
stability: experimental
description: "Run requirement interviews with prepared question ladders, recorded answers, and explicit confirmation of each elicited requirement."
added: "2026-10"
version: v1
related: [clarification-seeking, question-answering, audience-analysis]
tags: [requirements, interviewing, process]
---

# Requirement Elicitation Interviewing

## Description
Run requirement interviews with prepared question ladders, recorded answers, and explicit confirmation of each elicited requirement. The procedure is constrained by explicit inputs and acceptance criteria rather than best-effort judgment alone.

## When to Use
- requirements are vague and stakeholders must be interviewed before work can be planned.
- Ambiguity or missing evidence would change the outcome.
- The result must be recorded with reasons and evidence for later verification.

## Inputs / Outputs
| Area | Contract |
|---|---|
| Inputs | Task context, candidate inputs, and explicit acceptance criteria for requirement elicitation interviewing work. |
| Outputs | A decision or artifact with recorded reasons, rejected alternatives, and verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Define the goal, the constraints, and the boundary of what this procedure may change.
2. Inventory the available inputs and flag gaps or ambiguities that block progress.
3. Execute the requirement elicitation interviewing steps in a bounded, checkpointed way.
4. Compare the actual outcome against the expected outcome and record deviations.
5. On failure, apply the declared fallback path, and never widen permissions to recover.
6. Emit a structured result with evidence and provenance for downstream consumers.

## Runnable Example
```python
def summarize(answers):
    confirmed, open_q = [], []
    for a in answers:
        (confirmed if a["status"] == "confirmed" else open_q).append(a["topic"])
    return {"confirmed": confirmed, "open": open_q}

ans = [{"topic": "sso", "status": "confirmed"}, {"topic": "retention", "status": "open"}]
s = summarize(ans)
assert s["confirmed"] == ["sso"] and s["open"] == ["retention"]
```

## Failure Modes
- Asking leading questions that bake in the answer.
- Not recording who answered and when.
- Ending the interview without confirming each requirement.
- Mixing solution ideas with actual requirements.
- No follow-up loop for unanswered questions.

## Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result.

## Evidence
Requirement clarity before agent implementation is a recurring 2026 project failure topic in public discussion; this is a dated signal, not an adoption metric.

## Related
- clarification-seeking.md
- question-answering.md
- audience-analysis.md
