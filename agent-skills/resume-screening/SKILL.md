---
name: resume-screening
description: Screen resumes against a written rubric with per-criterion evidence spans, anchored scoring, and explicit missing-information handling so ranking decisions stay auditable and bias-controlled.
metadata:
  source: skills/16-domain-specific/resume-screening.md
  category: 16-domain-specific
  version: "v1"
---

# Resume Screening

Category: Domain-Specific | Level: intermediate | Stability: experimental | Version: v1

## Description

Resume screening is a judgment task wrapped in an audit problem. The skill makes the judgment mechanical and the audit trivial: criteria are written before any resume is read, each criterion is scored only against quoted evidence from the document, missing information is recorded as missing rather than punished, and protected attributes are never inferred or used. The output is a structured verdict with provenance, not a ranking by feel.

## When to Use

Use when a stack of resumes must be reduced to a ranked or triaged shortlist against a defined role, and the decision must be explainable afterward.

Do not use to make hiring decisions; screening output is decision support that humans review before any candidate outcome.

## Inputs

| Input | Type | Required | Description |
|---|---|---|---|
| `resume_text` | `string` | Yes | The candidate document to screen |
| `rubric` | `list[criterion]` | Yes | Written criteria with anchored score levels |
| `role_requirements` | `map` | Yes | The role definition the rubric was derived from |

## Procedure

1. Fix the rubric before reading resumes; criteria written after reading a candidate are advocacy, not screening.
2. For each criterion, quote the evidence span from the resume that supports a score, or record it as missing.
3. Score against anchored levels defined in the rubric; two screeners should reach the same score from the same span.
4. Treat missing information as missing — a gap is not a negative unless the rubric says so explicitly.
5. Never infer protected attributes from text, dates, or names; they are out of scope by construction.
6. Emit the structured verdict with every span, score, and gap, so the decision can be reconstructed or challenged.

## Outputs

| Output | Type | Description |
|---|---|---|
| `verdict` | `map[criterion -> score]` | Per-criterion scores with anchors |
| `evidence` | `map[criterion -> span]` | The quoted text supporting each score |
| `gaps` | `list[criterion]` | Criteria the resume left unanswered |

## Runnable Example

```python
def score_resume(resume_text, rubric):
    """Score each criterion only from quoted evidence."""
    evidence, gaps = {}, []
    for criterion, keywords, score in rubric:
        hit = next((k for k in keywords if k in resume_text), None)
        if hit is None:
            gaps.append(criterion)
        else:
            evidence[criterion] = (score, hit)
    return evidence, gaps

rubric = [("python", ["python", "pytorch"], 2), ("sql", ["sql", "postgres"], 2),
          ("mentoring", ["mentored", "led team"], 1)]
text = "Strong python background; wrote postgres ETL pipelines."
evidence, gaps = score_resume(text, rubric)
print(evidence)
print(gaps)
```

## Failure Modes

| Failure Mode | Cause | Mitigation |
|---|---|---|
| Unanchored scoring | Scores reflect the screener's mood | Use rubric anchors any screener can apply |
| Punishing gaps | Missing information read as weakness | Record gaps as gaps unless the rubric penalizes them |
| Protected-attribute inference | Dates, names, or photos used as signals | Keep protected attributes out of scope by construction |
| Keyword-only matching | Exact terms trump equivalent experience | Match synonyms defined in the rubric; keep humans in review |
| Decision without provenance | Verdict with no quoted evidence | Emit spans with every score or the verdict is invalid |

## Security and Authority Boundary

Screening output is decision support for a human decision governed by employment law and fairness review. Bias auditing, adverse-impact analysis, and candidate communication remain with the hiring process, not with the screener.

## Evidence

This skill is grounded in dated public implementation references:

1. Wikipedia's overview of applicant tracking systems (https://en.wikipedia.org/wiki/Applicant_tracking_system).
2. Wikipedia's overview of the curriculum vitae as a document (https://en.wikipedia.org/wiki/Curriculum_vitae).

Honest boundary: these are implementation references, not adoption or demand evidence; this entry was added under the owner-directed corpus expansion recorded in `meta/memory/DECISIONS.md`, and no demand signal is claimed for it.

## Related Skills

- [Essay Grading](essay-grading.md) — the same rubric-and-evidence discipline applied to grading.
- [Data Labeling](data-labeling.md) — label-level quality control these judgments feed.

## Changelog

| Date | Version | Change |
|---|---|---|
| `2026-10` | v1 | Initial entry added under the owner-directed corpus expansion |
