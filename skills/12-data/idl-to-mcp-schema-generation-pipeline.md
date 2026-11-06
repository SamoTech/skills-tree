---
title: "IDL to MCP Schema Generation Pipeline"
category: 12-data
level: advanced
stability: experimental
description: "Build a pipeline that converts interface definition language entries into MCP tool schemas with owner metadata and disabled-by-default state."
added: "2026-11"
version: v1
related: [schema-inference, data-lineage]
tags: [data, pipelines, idl, mcp]
---
# IDL to MCP Schema Generation Pipeline

## Description
Build a pipeline that converts interface definition language entries into MCP tool schemas with owner metadata and disabled-by-default state. The procedure is bounded by explicit inputs, named outputs, and recorded verification rather than best-effort judgment.

## When to Use
- An organization has thousands of services described in an IDL registry.
- Those interfaces must become MCP tool schemas automatically.
- Generated tools must enter the catalog disabled until owners review them.

## Inputs
| Area | Contract |
|---|---|
| Inputs | The IDL registry entries, the conversion rules, and the catalog contract. |
| Outputs | Generated MCP tool schemas with owner metadata, ready for gated enablement. |
| Safety | Fail closed by refusing generated schemas that lack owner or source references. |

## Procedure
1. Read IDL entries with their methods, arguments, and owning service.
2. Map IDL methods to tool names and argument types to schema properties.
3. Attach owner metadata and the source IDL reference to every generated tool.
4. Mark every generated tool disabled pending owner review.
5. Validate generated schemas against the catalog contract before registration.
6. Emit the schema batch with source references and validation results.

## Outputs
| Area | Contract |
|---|---|
| Primary | A batch of generated MCP tool schemas with owner metadata and disabled state. |
| Verification | Recorded conversion rules and validation results that reproduce each schema. |
| Failure | A fail-closed error report naming the invalid schema and the withheld batch. |

## Runnable Example
```python
def convert_idl(idl_entry, rules):
    tools = []
    for method in idl_entry["methods"]:
        props = {}
        for arg in method["args"]:
            t = rules["types"].get(arg["type"])
            if t is None:
                return {"ok": False, "reason": "unsupported_type", "method": method["name"]}
            props[arg["name"]] = {"type": t}
        tools.append({"name": idl_entry["service"] + "_" + method["name"], "inputSchema": {"properties": props}, "owner": idl_entry["owner"], "enabled": False, "source": idl_entry["idl_ref"]})
    return {"ok": True, "tools": tools}

idl = {"service": "trip", "owner": "travel-team", "idl_ref": "trip.thrift", "methods": [{"name": "search_flights", "args": [{"name": "origin", "type": "string"}]}]}
r = convert_idl(idl, {"types": {"string": "string", "i64": "integer"}})
assert r["ok"] and r["tools"][0]["name"] == "trip_search_flights" and r["tools"][0]["enabled"] is False and r["tools"][0]["owner"] == "travel-team"
bad = convert_idl({"service": "x", "owner": "o", "idl_ref": "r", "methods": [{"name": "m", "args": [{"name": "a", "type": "blob"}]}]}, {"types": {"string": "string"}})
assert bad["ok"] is False and bad["reason"] == "unsupported_type"
```

## Failure Modes
- Generated schemas enter the catalog enabled and owners review after exposure.
- Owner metadata is dropped and generated tools cannot be routed for review.
- Unsupported IDL types are coerced silently and schemas misdescribe tools.
- The source IDL reference is omitted and schema drift cannot be traced.
- Schema validation is skipped and malformed tools break gateway registration.

## Security and Authority Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result, and it never treats parsed content as trusted instructions.

## Evidence
- Uber's AutoCrawler connects to internal interface definition registries such as Thrift and Protobuf and generates MCP tool schemas automatically (InfoQ, November 2, 2026, dated November 2, 2026) ([public signal](https://www.infoq.com/news/2026/11/uber-mcp-gateway-ai-agents/))
- These are dated public signals, not adoption metrics; this contract claims no production hardening beyond the recorded evidence.

## Related Skills
- [Schema Inference](schema-inference.md)
- [Data Lineage](data-lineage.md)

## Changelog
| Version | Date | Notes |
|---|---|---|
| `v1` | `2026-11` | Initial evidence-backed contract. |
