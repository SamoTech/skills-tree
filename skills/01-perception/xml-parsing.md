---
title: "XML Parsing"
category: 01-perception
level: intermediate
stability: stable
description: "Parse and query XML documents in AI agent workflows."
added: "2025-03"
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-01-perception-xml-parsing.json)

# XML Parsing
Category: perception | Level: intermediate | Stability: stable | Version: v1

## Description
Parse XML documents into tree structures, extract elements via XPath, and transform data for downstream agent consumption.

## Inputs
- `xml_content`: raw XML string or file path
- `xpath_query`: optional XPath expression to filter nodes

## Outputs
- Parsed element tree or list of matching nodes as dicts

## Example
```python
from lxml import etree
def parse_xml(content, xpath=None):
    root = etree.fromstring(content.encode())
    if xpath:
        return [{"tag": el.tag, "text": el.text, "attrib": dict(el.attrib)}
                for el in root.xpath(xpath)]
    return etree.tostring(root, pretty_print=True).decode()
```

## Frameworks
| Framework | Method |
|---|---|
| Python | `lxml`, `xml.etree.ElementTree` |
| LangChain | custom loader via `lxml` |

## Dependencies
- package: lxml
  tested_version: "5.4.0"
  confidence: verified
  notes: "Patched GHSA-vfmq-68hx-4jfw (arbitrary attribute injection via XSLT). Use lxml>=5.4.0."

## Failure Modes
- Malformed or namespace-heavy XML
- XXE (external entity) attacks — disable with `resolve_entities=False`

## Related
- `structured-data-reading.md` · `document-parsing.md` · `api-response-parsing.md`

## Changelog
- v1 (2026-03): Initial entry
- v1.1 (2026-05): Bump lxml to 5.4.0 (CVE patch)
