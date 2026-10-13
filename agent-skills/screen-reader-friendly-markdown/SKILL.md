---
name: screen-reader-friendly-markdown
description: Write markdown that screen readers announce cleanly by using correct heading levels, alt text, and table semantics with no layout-only markup.
metadata:
  source: skills/06-communication/screen-reader-friendly-markdown.md
  category: 06-communication
  version: "v1"
---

# Screen Reader Friendly Markdown

## Description
Write markdown that screen readers announce cleanly by using correct heading levels, alt text, and table semantics with no layout-only markup. The procedure is constrained by explicit inputs and acceptance criteria rather than best-effort judgment alone.

## When to Use
- documents must be accessible to screen reader users before publishing.
- Ambiguity or missing evidence would change the outcome.
- The result must be recorded with reasons and evidence for later verification.

## Inputs / Outputs
| Area | Contract |
|---|---|
| Inputs | Task context, candidate inputs, and explicit acceptance criteria for screen reader friendly markdown work. |
| Outputs | A decision or artifact with recorded reasons, rejected alternatives, and verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Define the goal, the constraints, and the boundary of what this procedure may change.
2. Inventory the available inputs and flag gaps or ambiguities that block progress.
3. Execute the screen reader friendly markdown steps in a bounded, checkpointed way.
4. Compare the actual outcome against the expected outcome and record deviations.
5. On failure, apply the declared fallback path, and never widen permissions to recover.
6. Emit a structured result with evidence and provenance for downstream consumers.

## Runnable Example
```python
def accessibility_issues(doc):
    issues = []
    if "![alt]" in doc or "!(alt)" in doc:
        issues.append("empty-alt-text")
    if doc.count("####") > 6:
        issues.append("deep-heading-nesting")
    if "|" in doc and "|---" not in doc:
        issues.append("table-without-header-row")
    return issues

assert accessibility_issues("![alt](x.png)\ntext") == ["empty-alt-text"]
assert accessibility_issues("# Title\n| a |\n|---|\n") == []
```

## Failure Modes
- Skipping heading levels to make text look smaller.
- Empty or decorative alt text on informative images.
- Tables without header rows.
- Conveying meaning only through color or emoji.
- Testing only visually, never with a reader.

## Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result.

## Evidence
Accessibility requirements for generated content are a recurring 2026 compliance topic in public coverage; this is a dated signal, not an adoption metric.

## Related
- structured-output.md
- plain-language-writing.md
- faq-generation.md
