---
title: "XML Parsing"
category: 01-perception
level: intermediate
stability: stable
description: "Apply xml parsing in AI agent workflows."
added: "2025-03"
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-01-perception-xml-parsing.json)

# XML Parsing
Category: perception | Level: basic | Stability: stable | Version: v1

## Description
Parse XML/HTML documents into navigable trees, extracting elements, attributes, and text nodes.

## Inputs
- `source`: XML string, file path, or URL
- `query`: XPath or CSS selector

## Outputs
- Matched elements as list of dicts

## Example
```python
from lxml import etree
tree = etree.parse("data.xml")
results = tree.xpath("//product[@active='true']/name/text()")
print(results)  # ['Widget A', 'Widget B']
```

## Frameworks
| Framework | Method |
|---|---|
| Python | `lxml`, `xml.etree.ElementTree` |
| LangChain | `BSHTMLLoader` |
| BeautifulSoup | `find_all()` with CSS selectors |

## Failure Modes
- Malformed XML breaks strict parsers (use `recover=True` in lxml)
- Namespace prefixes in XPath require explicit registration

## Related
- `document-parsing.md` · `api-response-parsing.md`

## Changelog
- v1 (2026-04): Initial entry
