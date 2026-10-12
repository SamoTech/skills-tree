---
title: "Receipt Parsing"
category: 16-domain-specific
level: intermediate
stability: experimental
description: "Extract merchant, date, line item, tax, and total fields from raw receipt text with arithmetic cross-checks so expense records rest on validated numbers rather than best guesses."
added: "2026-10"
version: v1
related: ["invoice-processing", "financial-statement"]
---

# Receipt Parsing

Category: Domain-Specific | Level: intermediate | Stability: experimental | Version: v1

## Description

A receipt is unstructured text pretending to be a table. Parsing it means segmentation (header, items, totals), normalization (dates, currencies, decimal separators per locale), and — the part that separates data from guesswork — arithmetic verification: line items must sum to the subtotal, and subtotal plus tax must match the stated total. Every extracted field carries its raw span, so any number in the structured record can be traced to where it came from.

## When to Use

Use when receipt text (typed or OCR output) must become structured expense data — bookkeeping automation, reimbursement workflows, spend analysis.

Do not use when a structured source exists instead; supplier invoices with structured input are a stricter field contract handled by invoice processing.

## Inputs

| Input | Type | Required | Description |
|---|---|---|---|
| `receipt_text` | `string` | Yes | Raw or OCR-extracted receipt text |
| `locale` | `string` | Yes | Expected date, currency, and number formats |
| `required_fields` | `list[field]` | Yes | Fields the caller needs to be present |

## Procedure

1. Segment the text: header block, line-item block, totals block; totals are parsed from the bottom up, where receipts are most structured.
2. Normalize numbers per locale — decimal separator, currency symbol, thousands grouping — before any arithmetic.
3. Parse line items as (quantity, description, amount) triples; wrapped descriptions are joined, not split into items.
4. Cross-check: item sum against stated subtotal; subtotal plus tax against stated total; record the verdict per check.
5. When a stated total is missing, compute it and flag it as computed, never as extracted.
6. Output the structured record with per-field raw spans and confidence; unresolved fields are flagged, not invented.

## Outputs

| Output | Type | Description |
|---|---|---|
| `record` | `map[field -> value]` | Merchant, date, items, subtotal, tax, total |
| `checks` | `list[(check, verdict)]` | Arithmetic cross-check results |
| `unresolved` | `list[field]` | Fields that could not be extracted |

## Runnable Example

```python
import re

def parse_items(receipt_text, pattern=r"^(.+?)\s+(\d+[.,]\d{2})$"):
    items = []
    for line in receipt_text.splitlines():
        match = re.match(pattern, line.strip())
        if match:
            items.append((match.group(1), float(match.group(2).replace(",", "."))))
    return items

def cross_check(items, stated_subtotal):
    computed = round(sum(amount for _, amount in items), 2)
    return computed, abs(computed - stated_subtotal) < 0.01

text = "Coffee 4.50\nCake 3.20\nSubtotal 7.70\nTax 0.77\nTotal 8.47"
items = parse_items(text)
print(items)
print(cross_check(items, stated_subtotal=7.70))
```

## Failure Modes

| Failure Mode | Cause | Mitigation |
|---|---|---|
| OCR digit noise | Misread digits pass the regex but fail arithmetic | Run cross-checks; flag records whose math fails |
| Locale confusion | `1.234,56` parsed as `1.23` | Normalize per the declared locale first |
| Split line items | Wrapped descriptions become two items | Join continuation lines before matching |
| Missing totals | Stated total absent from the slip | Compute and mark as computed, never as extracted |
| Tax-inclusive pricing | Totals include tax the parser assumed was added | Detect tax-inclusive slips and adjust the checks |

## Security and Authority Boundary

Parsed receipts are structured data for review, not financial records of record. Reimbursement approval, tax treatment, and fraud detection remain with the accounting workflow and its human checks.

## Evidence

This skill is grounded in dated public implementation references:

1. Wikipedia's overview of receipts as transaction records (https://en.wikipedia.org/wiki/Receipt).
2. The Python standard library documentation for the re module (https://docs.python.org/3/library/re.html).

Honest boundary: these are implementation references, not adoption or demand evidence; this entry was added under the owner-directed corpus expansion recorded in `meta/memory/DECISIONS.md`, and no demand signal is claimed for it.

## Related Skills

- [Invoice Processing](invoice-processing.md) — the stricter field-contract sibling for supplier invoices.
- [Financial Statement](financial-statement.md) — downstream financial documents that consume these records.

## Changelog

| Date | Version | Change |
|---|---|---|
| `2026-10` | v1 | Initial entry added under the owner-directed corpus expansion |
