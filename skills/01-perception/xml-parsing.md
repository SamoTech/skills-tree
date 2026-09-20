---
title: "XML Parsing"
category: 01-perception
level: intermediate
stability: stable
description: "Parse untrusted XML with bounded, non-expanding semantics and deterministic element extraction while preventing external-entity and network resolution."
added: "2025-03"
version: v2
related: [structured-data-reading, document-parsing, api-response-parsing, file-system-reading]
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-01-perception-xml-parsing.json)

# XML Parsing
Category: perception | Level: intermediate | Stability: stable | Version: v2

## Description
XML parsing converts an XML document into a tree and optionally extracts matching elements. XML is an input format, not an instruction channel. The parser must therefore reject or disable external entities, network access, and other expansion behavior that can turn a small document into excessive work or unexpected data access.

Use the standard-library implementation when the task only requires bounded local XML parsing. Use `lxml` when XPath support is required, but keep parser configuration explicit and pinned by the execution environment.

## Inputs
- `xml_content`: UTF-8 XML bytes or string.
- `xpath_query`: optional local XPath expression when using an XPath-capable parser.
- `max_bytes`: optional positive input bound applied before parsing.
- `max_results`: optional positive extraction bound.

## Outputs
- `root`: parsed root element for local processing.
- `matches`: ordered extracted element records when an XPath query is used.
- `truncated`: whether the input exceeded the explicit byte bound.

## Deterministic reference implementation
```python
import xml.etree.ElementTree as ET


def parse_xml(xml_content, *, max_bytes=1_000_000, max_results=1000):
    if max_bytes <= 0 or max_results <= 0:
        raise ValueError("bounds must be positive")
    raw = xml_content.encode("utf-8") if isinstance(xml_content, str) else bytes(xml_content)
    truncated = len(raw) > max_bytes
    if truncated:
        raise ValueError("XML input exceeds max_bytes; do not parse a partial document")

    root = ET.fromstring(raw)
    matches = []
    for element in root.iter():
        if len(matches) >= max_results:
            raise ValueError("XML result limit exceeded")
        matches.append({
            "tag": element.tag,
            "text": element.text,
            "attributes": dict(element.attrib),
        })
    return {"root": root, "matches": matches, "truncated": False}


result = parse_xml('<root><item id="1">A</item></root>')
assert result["matches"][1]["attributes"]["id"] == "1"
```

## Contract
| Input condition | Required behavior | Output invariant |
|---|---|---|
| Valid local XML | Parse deterministically | Stable element order |
| Oversized XML | Reject before parsing | No partial-document parse |
| Malformed XML | Raise parse error | No fabricated tree |
| Too many results | Stop with explicit error | Bounded output |
| External entity declaration | Do not resolve it | No network/file expansion |
| Untrusted XPath | Treat as a query, not executable code | No dynamic code evaluation |

## XPath guidance
XPath is useful for selecting elements, but callers should keep expressions simple and deterministic. Validate namespace mappings explicitly. Do not concatenate untrusted values into XPath expressions when a parameterized or escaped query mechanism is available.

When `lxml` is required, construct the parser with external entity and network resolution disabled and avoid unsafe XSLT execution. The exact hardening settings must be tested against the installed `lxml` version rather than copied blindly between versions.

## Failure Modes
| Failure | Detection | Mitigation |
|---|---|---|
| Malformed XML | `ET.ParseError` | Reject input and report location where available |
| Oversized document | Byte bound exceeded | Stream or reject before parsing |
| Entity expansion risk | DTD/entity input detected | Use hardened parser configuration and reject unsafe constructs |
| Namespace mismatch | Empty query result | Supply explicit namespace map |
| Result explosion | `max_results` reached | Increase bound deliberately or narrow the query |
| Encoding mismatch | Decode/parse error | Validate declared encoding and preserve original bytes |

## Security boundaries
Do not enable external entity resolution for untrusted documents. Do not permit network access from the XML parser. Do not apply XSLT supplied by untrusted input. Parsing success does not establish that the document is trustworthy; provenance and content validation remain caller responsibilities.

## Frameworks
| Framework | Method |
|---|---|
| Python | `xml.etree.ElementTree` for local bounded parsing |
| Python | `lxml.etree` for XPath with explicit hardening |
| LangChain | Custom XML loader backed by a hardened parser |

## Dependencies
- package: lxml
  tested_version: "5.4.0"
  confidence: verified
  notes: "Optional for XPath. The reference implementation uses the Python standard library."

## Related
- `structured-data-reading.md`
- `document-parsing.md`
- `api-response-parsing.md`
- `file-system-reading.md`

## Changelog
- v1 (2026-03): Initial entry
- v1.1 (2026-05): Bump lxml to 5.4.0
- v2 (2026-09): Added bounded parsing, deterministic reference code, explicit security boundaries, and failure-mode contract.
