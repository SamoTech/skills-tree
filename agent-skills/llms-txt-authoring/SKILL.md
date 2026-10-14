---
name: llms-txt-authoring
description: Author llms.txt markdown overviews and per-page llms-full.txt variants so AI crawlers get curated site guidance.
metadata:
  source: skills/11-web/llms-txt-authoring.md
  category: 11-web
  version: "v1"
---
# Llms Txt Authoring

## Description
Author llms.txt markdown overviews and per-page llms-full.txt variants so AI crawlers get curated site guidance. The procedure is constrained by explicit inputs and acceptance criteria rather than best-effort judgment alone.

## When to Use
- A task requires llms txt authoring before downstream steps can proceed safely.
- Ambiguity or missing evidence would change the outcome.
- The result must be recorded with reasons and evidence for later verification.

## Inputs / Outputs
| Area | Contract |
|---|---|
| Inputs | Task context, candidate inputs, and explicit acceptance criteria for llms txt authoring. |
| Outputs | A decision or artifact with recorded reasons, rejected alternatives, and verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Define the goal, the constraints, and the boundary of what this procedure may change.
2. Inventory the available inputs and flag gaps or ambiguities that block progress.
3. Execute the llms txt authoring steps in a bounded, checkpointed way.
4. Compare the actual outcome against the expected outcome and record deviations.
5. On failure, apply the declared fallback path, and never widen permissions to recover.
6. Emit a structured result with evidence and provenance for downstream consumers.

## Runnable Example
```python
def llms_txt(title, overview, links):
    body = "# %s\n\n> %s\n\n" % (title, overview)
    body += "".join("- [%s](%s)\n" % (n, h) for n, h in links)
    return body
txt = llms_txt("Docs", "Site overview", [("Home", "/")])
assert "# Docs" in txt and "/)" in txt
```

## Failure Modes
- Acting outside the declared task boundary.
- Assuming an estimate or preview equals the verified effect.
- Retrying without preserving state or evidence.
- Using stale inputs as if they were current.
- Reporting success without checking the resulting state.

## Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result.

## Evidence
llms.txt adoption for AI-crawler guidance is a recurring 2026 website publishing request. These are dated public signals, not adoption metrics.

## Related
- markdown-parsing.md
- html-reading.md
- metadata-extraction.md
