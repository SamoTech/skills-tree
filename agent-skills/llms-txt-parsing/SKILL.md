---
name: llms-txt-parsing
description: Fetch and parse llms.txt files into a structured resource inventory with syntax validation before any listed resource is fetched.
metadata:
  source: skills/11-web/llms-txt-parsing.md
  category: 11-web
  version: "v1"
---

# llms.txt Parsing

## Description
Fetch and parse llms.txt files into a structured resource inventory with syntax validation before any listed resource is fetched. The procedure is constrained by explicit inputs and acceptance criteria rather than best-effort judgment alone.

## When to Use
- a site publishes an llms.txt file and an agent needs its guidance before crawling.
- Ambiguity or missing evidence would change the outcome.
- The result must be recorded with reasons and evidence for later verification.

## Inputs / Outputs
| Area | Contract |
|---|---|
| Inputs | Task context, candidate inputs, and explicit acceptance criteria for llms.txt parsing work. |
| Outputs | A decision or artifact with recorded reasons, rejected alternatives, and verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Define the goal, the constraints, and the boundary of what this procedure may change.
2. Inventory the available inputs and flag gaps or ambiguities that block progress.
3. Execute the llms.txt parsing steps in a bounded, checkpointed way.
4. Compare the actual outcome against the expected outcome and record deviations.
5. On failure, apply the declared fallback path, and never widen permissions to recover.
6. Emit a structured result with evidence and provenance for downstream consumers.

## Runnable Example
```python
def parse_llms_txt(text):
    sections = {}
    current = None
    for line in text.splitlines():
        if line.startswith('# '):
            current = line[2:].strip()
            sections[current] = []
        elif current and line.strip():
            sections[current].append(line.strip())
    if 'Docs' not in sections:
        raise ValueError('required Docs section missing')
    return sections

txt = '# Docs\n- link: Home\n# Optional\n- link: Blog'
assert parse_llms_txt(txt)['Docs'] == ['- link: Home']
```

## Failure Modes
- Trusting a parsed file whose declared sections were never validated.
- Fetching listed resources without checking the declared permissions.
- Ignoring fetch errors for linked resources and continuing.
- Parsing a stale cached copy as if current.
- Treating optional sections as required and rejecting valid files.

## Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result.

## Evidence
llms.txt adoption for agent-facing site guidance grew through 2026; this is a dated signal, not an adoption metric.

## Related
- robots-txt-parsing.md
- sitemap-parsing.md
- url-fetching.md
