---
title: "Contract Reading"
category: 01-perception
level: intermediate
stability: stable
version: v2
description: "Extract contract structure, parties, dates, obligations, definitions, and termination or payment clauses while preserving source spans and uncertainty. Use it for document analysis, not as a substitute for legal advice or legal review."
added: "2025-03"
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-01-perception-contract-reading.json)

# Contract Reading
Category: perception | Level: advanced | Stability: stable | Version: v1

## Description
Extract key clauses, parties, dates, and obligations from legal contracts using LLM-assisted parsing.

## Inputs
- `document`: contract text or PDF path
- `extract_fields`: list of fields (e.g., `["parties", "effective_date", "termination_clause"]`)

## Outputs
- Structured dict with extracted field values and source spans

## Example
```python
import anthropic
client = anthropic.Anthropic()
with open("contract.txt") as f:
    text = f.read()
response = client.messages.create(
    model="claude-opus-4-5",
    max_tokens=2048,
    messages=[{"role": "user", "content": f"Extract: parties, effective_date, payment_terms, termination_clause from:\n{text[:4000]}\nReturn JSON."}]
)
import json
fields = json.loads(response.content[0].text)
```

## Frameworks
| Framework | Method |
|---|---|
| LlamaIndex | `StructuredLLMExtractor` |
| LangChain | `create_extraction_chain()` |
| Raw API | Structured output prompt |

## Failure Modes
- Defined terms redefined mid-document
- Exhibits/schedules referenced but not included

## Related
- `document-parsing.md` · `pdf-parsing.md`

## Changelog
- v1 (2026-04): Initial entry


## Evidence

The skill's implementation guidance is grounded in the following primary references:
- Agent Skills specification: https://agentskills.io/specification
- Python JSON tooling for structured extraction: https://docs.python.org/3/library/json.html

Evidence status: implementation guidance verified against the cited documentation; no benchmark claim is made unless a reproducible benchmark is included in this file.
