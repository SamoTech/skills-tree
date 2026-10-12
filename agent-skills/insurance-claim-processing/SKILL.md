---
name: insurance-claim-processing
description: Intake, validate, and adjudicate insurance claims against policy terms and document evidence, producing a decision trail with coverage determination, deduction, and reserve notes.
metadata:
  source: skills/16-domain-specific/insurance-claim-processing.md
  category: 16-domain-specific
  version: "v1"
---

# Insurance Claim Processing

Category: Domain-Specific | Level: intermediate | Stability: experimental | Version: v1

## Description

Claim processing is evidence work under contract terms. The skill covers structured intake of claim forms and supporting documents, extracting the loss facts into a typed record, validating coverage against the policy terms in force at loss date, applying limits and deductibles, and emitting a decision trail that ties every conclusion to the clause or document that supports it. Ambiguity is surfaced, not smoothed.

## When to Use

Use when first-notice-of-loss data, claim forms, and supporting documents must be converted into a coverage determination or a preparation package for an adjuster.

Do not auto-deny on missing paperwork without disclosure. An incomplete file is a follow-up task; a denial is a coverage decision with consequences.

## Inputs

| Input | Type | Required | Description |
|---|---|---|---|
| `claim_file` | `table` | Yes | Claim intake data: peril, date, description, claimant |
| `documents` | `table` | Yes | Supporting documents: photos, receipts, reports, statements |
| `policy_terms` | `object` | Yes | Coverage terms, limits, deductibles, and exclusions at loss date |

## Procedure

1. Normalize the intake record: peril, loss date, location, claimant, and described damages.
2. Extract evidence from supporting documents into typed facts with document provenance.
3. Match the loss against policy coverage at loss date, including applicable exclusions.
4. Apply limits and deductibles arithmetically and show the calculation in the record.
5. Flag ambiguities and missing evidence as follow-ups, distinct from coverage decisions.
6. Emit the decision trail: determination, amounts, and the clause or document behind each.

## Outputs

| Output | Type | Description |
|---|---|---|
| `claim_record` | `object` | Typed loss facts with document provenance per fact |
| `coverage_determination` | `object` | Coverage decision with applied clauses and exclusions |
| `follow_ups` | `list` | Missing evidence and ambiguities requiring human handling |

## Runnable Example

```python
def apply_deductible(claim_amount, deductible, limit):
    if claim_amount <= deductible:
        payable = 0.0
    else:
        payable = min(claim_amount - deductible, limit)
    return {"claimed": claim_amount, "deductible": deductible,
            "payable": round(payable, 2), "capped_by_limit": claim_amount - deductible > limit}

print(apply_deductible(claim_amount=12500.0, deductible=1000.0, limit=10000.0))
```

## Failure Modes

| Failure Mode | Cause | Mitigation |
|---|---|---|
| Wrong policy version applied | Terms pulled at processing date, not loss date | Bind coverage terms to the loss date explicitly |
| Exclusion skipped | Exclusion clauses not checked against loss facts | Match loss facts against every exclusion clause |
| Evidence-free conclusions | Facts inferred without document support | Require provenance per extracted fact |
| Silent auto-denial | Missing paperwork treated as coverage denial | Separate follow-ups from determinations |
| Arithmetic opacity | Payable amount without visible calculation | Show limits, deductibles, and steps in the record |

## Security and Authority Boundary

Claims combine medical, financial, and personal data under regulatory protection. Restrict access per role, keep adjuster notes separate from automated extractions, and never let automated processing issue denials without a human reviewer in regulated jurisdictions.

## Evidence

This skill is grounded in dated public implementation references:

1. The National Association of Insurance Commissioners resources on claim handling standards (https://www.naic.org/).
2. The Wikipedia article on insurance as the domain this procedure operates in (https://en.wikipedia.org/wiki/Insurance).

Honest boundary: these are implementation references, not adoption or demand evidence; this entry was added under the owner-directed corpus expansion recorded in `meta/memory/DECISIONS.md`, and no demand signal is claimed for it.

## Related Skills

- [Invoice Processing](invoice-processing.md) — the document extraction machinery shared with claim paperwork.
- [Compliance Checking](compliance-checking.md) — the regulatory gate every coverage determination must pass.

## Changelog

| Date | Version | Change |
|---|---|---|
| `2026-10` | v1 | Initial entry added under the owner-directed corpus expansion |
