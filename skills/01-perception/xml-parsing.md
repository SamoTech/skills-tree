---
title: "XML Parsing"
category: 01-perception
level: intermediate
stability: stable
description: "Parse bounded XML safely into deterministic element data, preserve namespaces when required, and reject external-resource behavior before content reaches downstream agent logic."
added: "2025-03"
version: v2
related: [structured-data-reading, document-parsing, api-response-parsing]
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-01-perception-xml-parsing.json)

# XML Parsing
Category: perception | Level: intermediate | Stability: stable | Version: v2

## Description
XML parsing converts a bounded XML document into a tree and extracts selected elements.
The skill is deliberately limited to parsing and querying; transport, authentication, business semantics, and persistence remain outside its boundary.
For untrusted XML, use a hardened parser configuration or a maintained safe-XML library rather than enabling external entities.

## Inputs / Outputs
| Input | Type | Contract |
|---|---|---|
| `xml_content` | `str | bytes` | Complete, bounded XML document |
| `xpath` | `str | None` | Optional ElementTree-compatible path for local selection |
| `max_bytes` | `int` | Positive upper bound applied before parsing |

| Output | Type | Contract |
|---|---|---|
| `records` | `list[dict]` | Ordered element records containing tag, text, and attributes |
| `root_tag` | `str` | Root element tag for the parsed document |

## Deterministic Reference Implementation
```python
from xml.etree import ElementTree as ET


def parse_xml(xml_content, xpath=None, max_bytes=1_000_000):
    if max_bytes <= 0:
        raise ValueError("max_bytes must be positive")
    raw = xml_content.encode("utf-8") if isinstance(xml_content, str) else xml_content
    if not isinstance(raw, bytes):
        raise TypeError("xml_content must be str or bytes")
    if len(raw) > max_bytes:
        raise ValueError("XML input exceeds max_bytes")
    root = ET.fromstring(raw)
    nodes = root.findall(xpath) if xpath else [root]
    return {
        "root_tag": root.tag,
        "records": [
            {"tag": node.tag, "text": node.text or "", "attributes": dict(node.attrib)}
            for node in nodes
        ],
    }

result = parse_xml("<items><item id='1'>alpha</item></items>", "item")
assert result["records"][0]["text"] == "alpha"
```

## Namespaces
ElementTree expands namespace-qualified tags to `{uri}local` names.
Do not strip namespaces merely to make matching easier; doing so can merge distinct vocabularies.
For XPath-like queries, pass an explicit namespace mapping when the selected library supports it.
Treat namespace URIs as data, not as permission to fetch network resources.

## Frameworks
| Framework | Role | Security boundary |
|---|---|---|
| Python `xml.etree.ElementTree` | Lightweight deterministic parsing | Keep input bounded; do not assume it is a full security policy |
| `lxml` | Rich XPath and XML features | Use a hardened parser configuration for untrusted input |
| LangChain | Loader orchestration | XML security remains the parser's responsibility |

## Failure Modes
| Cause | Observable result | Mitigation |
|---|---|---|
| Malformed XML | `ParseError` | Reject and report location/context to caller |
| Input too large | `ValueError` | Enforce `max_bytes` before parsing |
| Namespace mismatch | Empty selection | Inspect expanded tag names and pass explicit namespaces |
| External-entity content | Unsafe or unexpected resolution in unsafe configurations | Disable external entity/network behavior; prefer hardened parsers |
| Mixed content | Important text appears in nested nodes | Define extraction rules instead of flattening blindly |

## Security Boundaries
XML is untrusted input. Parsing must not fetch external entities, schemas, stylesheets, DTDs, or URLs as a side effect.
Do not evaluate XSLT, XPath supplied by an untrusted caller, or embedded application-specific instructions without a separate policy layer.
The parser must not execute code or infer authorization from XML content.

## Validation Rules
- Reject non-`str`/`bytes` inputs.
- Enforce a finite input-size bound before parsing.
- Preserve document order in returned records.
- Return deterministic results for identical input and query.
- Keep network access and transport outside the parsing function.

## Provenance
The reference example uses Python's standard library and makes no claim about external parser CVE status.
If `lxml` or another dependency is selected, its deployed version and security advisories must be validated by the consuming project.

## Related
- `structured-data-reading.md` — generic structured records
- `document-parsing.md` — document-level extraction
- `api-response-parsing.md` — parsing structured HTTP response bodies

## Changelog
- v1 (2026-03): Initial entry
- v1.1 (2026-05): Dependency note updated for lxml
- v2 (2026-09-20): Added bounded reference parser, namespace guidance, explicit contracts, security boundaries, validation, and failure modes
