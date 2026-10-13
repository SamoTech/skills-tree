---
name: glossary-maintenance
description: Maintain a term glossary with one canonical definition per term, owner, review dates, and conflict checks so vocabulary stays consistent across documents.
metadata:
  source: skills/06-communication/glossary-maintenance.md
  category: 06-communication
  version: "v1"
---

# Glossary Maintenance

## Description
Maintain a term glossary with one canonical definition per term, owner, review dates, and conflict checks so vocabulary stays consistent across documents. The procedure is constrained by explicit inputs and acceptance criteria rather than best-effort judgment alone.

## When to Use
- documents drift because the same term is used with different meanings and the glossary must govern it.
- Ambiguity or missing evidence would change the outcome.
- The result must be recorded with reasons and evidence for later verification.

## Inputs / Outputs
| Area | Contract |
|---|---|
| Inputs | Task context, candidate inputs, and explicit acceptance criteria for glossary maintenance work. |
| Outputs | A decision or artifact with recorded reasons, rejected alternatives, and verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Define the goal, the constraints, and the boundary of what this procedure may change.
2. Inventory the available inputs and flag gaps or ambiguities that block progress.
3. Execute the glossary maintenance steps in a bounded, checkpointed way.
4. Compare the actual outcome against the expected outcome and record deviations.
5. On failure, apply the declared fallback path, and never widen permissions to recover.
6. Emit a structured result with evidence and provenance for downstream consumers.

## Runnable Example
```python
def conflicts(entries):
    seen = {}
    for e in entries:
        seen.setdefault(e["term"], set()).add(e["definition"])
    return {t: d for t, d in seen.items() if len(d) > 1}

entries = [
    {"term": "agent", "definition": "a"},
    {"term": "agent", "definition": "b"},
    {"term": "skill", "definition": "c"},
]
assert conflicts(entries) == {"agent": {"a", "b"}}
```

## Failure Modes
- Two definitions for one term with no owner to decide.
- Entries with no review date that silently rot.
- Defining terms by example instead of by boundary.
- Glossary not linked from the documents that use it.
- Merging glossaries without deduplication.

## Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result.

## Evidence
Shared vocabulary governance is a recurring 2026 documentation-quality topic in public discussion; this is a dated signal, not an adoption metric.

## Related
- citation-attribution.md
- paraphrasing.md
- plain-language-writing.md
