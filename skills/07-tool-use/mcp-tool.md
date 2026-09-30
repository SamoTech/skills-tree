---
title: "MCP Tool"
category: 07-tool-use
level: intermediate
stability: stable
description: "Expose or consume Model Context Protocol tools through explicit schemas, bounded permissions, and verified tool results."
added: "2026-09"
related: [07-tool-use, 14-security, 15-orchestration]
dependencies:
  - package: mcp
    min_version: "1.0.0"
    tested_version: "1.27.0"
    confidence: verified
---

# MCP Tool

## Description
Use the Model Context Protocol (MCP) to expose tools or connect an agent to MCP servers through a standardized tool interface. Tool names, descriptions, input schemas, permissions, and returned content must be treated as an explicit contract rather than inferred behavior.

## When to Use
- Expose a local or remote capability to an MCP-compatible client.
- Discover and invoke tools through an MCP server.
- Build an agent workflow that must remain portable across MCP-compatible clients.

## Inputs / outputs / failure modes

| Area | Guidance |
|---|---|
| Server | Identify the intended MCP server and transport before invocation. |
| Tool schema | Validate the declared name, description, and input schema. |
| Arguments | Construct only schema-valid arguments from trusted workflow state. |
| Permissions | Grant the minimum capability required by the task. |
| Output | Preserve structured content and distinguish errors from successful results. |
| Verification | Independently verify important side effects after a tool call. |
| Failure modes | Schema mismatch, unavailable server, transport failure, authorization error, or unsafe tool exposure. |

## Runnable Example

```python
# pip install mcp
from mcp.server.fastmcp import FastMCP

server = FastMCP("skills-tree-demo")

@server.tool()
def add(a: int, b: int) -> int:
    """Add two validated integers."""
    return a + b

if __name__ == "__main__":
    server.run()
```

## Failure modes
- Publishing a tool without an explicit input schema.
- Giving an MCP server access to secrets or destructive capabilities it does not need.
- Trusting tool descriptions as authorization.
- Treating a successful transport response as proof of a completed side effect.
- Failing to bound filesystem, network, or command execution capabilities.

## Evidence
- Model Context Protocol specification and documentation: https://modelcontextprotocol.io/
- Python MCP SDK documentation: https://github.com/modelcontextprotocol/python-sdk
- Repository schema and validation workflows define local conformance requirements.

## Related
- tool-guardrails
- function-calling
- approval-before-destructive-tools
- specialist-agent-routing
