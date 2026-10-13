---
name: developer-forum-answer-writing
description: Write forum answers that restate the problem, give a verified solution with steps, state limitations, and link sources.
metadata:
  source: skills/06-communication/developer-forum-answer-writing.md
  category: 06-communication
  version: "v1"
---

# Developer Forum Answer Writing

## Description
Write forum answers that restate the problem, give a verified solution with steps, state limitations, and link sources. The procedure is constrained by explicit inputs and acceptance criteria rather than best-effort judgment alone.

## When to Use
- a technical question is asked in a public forum and the answer must be verified and reusable.
- Ambiguity or missing evidence would change the outcome.
- The result must be recorded with reasons and evidence for later verification.

## Inputs / Outputs
| Area | Contract |
|---|---|
| Inputs | Task context, candidate inputs, and explicit acceptance criteria for developer forum answer writing work. |
| Outputs | A decision or artifact with recorded reasons, rejected alternatives, and verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Define the goal, the constraints, and the boundary of what this procedure may change.
2. Inventory the available inputs and flag gaps or ambiguities that block progress.
3. Execute the developer forum answer writing steps in a bounded, checkpointed way.
4. Compare the actual outcome against the expected outcome and record deviations.
5. On failure, apply the declared fallback path, and never widen permissions to recover.
6. Emit a structured result with evidence and provenance for downstream consumers.

## Runnable Example
```python
def answer(question, solution, verified):
    if not verified:
        raise ValueError("post only verified solutions")
    return f"Q: {question}\nA: {solution}"

assert answer("how to x", "run y", True).startswith("Q: how to x")
```

## Failure Modes
- Guessing an answer and marking it as a solution.
- Not stating the environment or versions tested.
- Link-only answers that rot when the link dies.
- Restating the question without solving it.
- Answering with untested copy-paste snippets.

## Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result.

## Evidence
Public developer support quality is a recurring 2026 community topic in public coverage; this is a dated signal, not an adoption metric.

## Related
- community-response-drafting.md
- question-answering.md
- citation-attribution.md
