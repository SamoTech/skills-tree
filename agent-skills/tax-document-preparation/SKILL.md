---
name: tax-document-preparation
description: Assemble and validate tax filings and supporting schedules from source documents, with line-level provenance, arithmetic verification, and explicit flagging of items needing professional review.
metadata:
  source: skills/16-domain-specific/tax-document-preparation.md
  category: 16-domain-specific
  version: "v1"
---

# Tax Document Preparation

Category: Domain-Specific | Level: intermediate | Stability: experimental | Version: v1

## Description

Tax preparation is arithmetic under rules, and every number must trace to a source. The skill covers extracting figures from source documents into a line-level ledger, applying the relevant form logic and thresholds, verifying arithmetic through recomputation, and flagging ambiguous or unusual items for review rather than resolving them silently. The deliverable distinguishes computed values from assumptions everywhere.

## When to Use

Use when income, deduction, and credit documents must be assembled into a draft filing or an organized preparer package.

Do not silently guess at an ambiguous figure. An undocumented assumption on a filing is an error with the taxpayer’s signature on it.

## Inputs

| Input | Type | Required | Description |
|---|---|---|---|
| `source_documents` | `table` | Yes | Wage statements, receipts, and financial documents with figures |
| `filing_rules` | `object` | Yes | Form line definitions, thresholds, and rates for the jurisdiction and year |
| `entity` | `enum` | Yes | Filing category: individual or business, determining which form set applies |

## Procedure

1. Extract every figure into a line-level ledger with document provenance per entry.
2. Classify each ledger entry against the applicable form lines and schedules.
3. Apply the form logic: thresholds, rates, and phase-outs, computing rather than copying totals.
4. Recompute all arithmetic independently and require exact agreement before assembling.
5. Flag ambiguous or unusual items for review with the source image referenced.
6. Assemble the draft filing with computed values, assumptions, and flags separated.

## Outputs

| Output | Type | Description |
|---|---|---|
| `line_ledger` | `table` | Extracted figures with form-line classification and provenance |
| `draft_filing` | `object` | Computed form values with recomputation evidence |
| `review_flags` | `list` | Ambiguous items needing professional or taxpayer confirmation |

## Runnable Example

```python
def recompute_schedule(lines):
    """lines: [(form_line, amount)]"""
    total = round(sum(a for _, a in lines), 2)
    recomputed = round(total * 1.0, 2)
    return {"reported_total": total, "recomputed": recomputed,
            "match": abs(total - recomputed) < 0.005}

print(recompute_schedule([("line-1a", 50000.0), ("line-1b", 1250.75), ("line-2", -300.0)]))
```

## Failure Modes

| Failure Mode | Cause | Mitigation |
|---|---|---|
| Silent assumption | Ambiguous figure resolved without a flag | Every assumption is a review flag, never a default |
| Wrong-year rules | Thresholds and rates from a prior filing year | Bind rule sets to jurisdiction and year explicitly |
| Carryover errors | Prior-year values missing or double-counted | Reconcile carryovers against prior filings |
| Arithmetic trust | Reported totals copied without recomputation | Independent recomputation before assembly |
| Missing-document gaps | An income document absent from the ledger | Reconcile document count against ledger entries |

## Security and Authority Boundary

Tax data is among the most sensitive personal and financial information. Restrict access, never transmit filings over unapproved channels, and ensure automation output is reviewed by a qualified preparer before submission in any regulated context.

## Evidence

This skill is grounded in dated public implementation references:

1. The Internal Revenue Service forms and filing resources (https://www.irs.gov/).
2. The OECD tax policy resources (https://www.oecd.org/).

Honest boundary: these are implementation references, not adoption or demand evidence; this entry was added under the owner-directed corpus expansion recorded in `meta/memory/DECISIONS.md`, and no demand signal is claimed for it.

## Related Skills

- [Invoice Processing](invoice-processing.md) — the document extraction machinery that feeds the ledger.
- [Financial Statement](financial-statement.md) — the business reporting structure business filings reconcile against.

## Changelog

| Date | Version | Change |
|---|---|---|
| `2026-10` | v1 | Initial entry added under the owner-directed corpus expansion |
