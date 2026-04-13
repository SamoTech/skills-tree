---
title: "Invoice Processing"
category: 16-domain-specific
level: advanced
stability: stable
description: "Apply invoice processing in AI agent workflows."
added: "2025-03"
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-16-domain-specific-invoice-processing.json)

**Category:** Domain-Specific
**Skill Level:** `advanced`
**Stability:** stable
**Added:** 2026-04

### Description
Extracts structured fields from vendor invoices (number, date, line items, totals, tax) using OCR and LLM parsing. Validates totals, currency, and dates before writing records to accounting or ERP systems.

### Example
```python
import anthropic, json, re

client = anthropic.Anthropic()

def parse_invoice(raw_text: str) -> dict:
    resp = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=512,
        messages=[{"role": "user", "content": (
            "Extract invoice fields as JSON: invoice_number, date, vendor, "
            "line_items (list of {description, qty, unit_price}), subtotal, tax, total.\n\n"
            + raw_text
        )}]
    )
    return json.loads(resp.content[0].text)

raw = "Invoice #INV-0042  Date: 2026-04-01  Vendor: Acme Corp\n"\
      "1x Cloud Server  $450.00  Tax 10%  Total $495.00"
print(parse_invoice(raw))
```

### Related Skills
- [OCR](../01-perception/ocr.md)
- [Document Parsing](../01-perception/document-parsing.md)
- [Data Cleaning](../12-data/data-cleaning.md)
