---
title: "MCP Tool"
category: 07-tool-use
level: intermediate
stability: stable
added: "2025-03"
description: "Apply MCP (Model Context Protocol) tools in AI agent workflows."
dependencies:
  - package: mcp
    min_version: "1.0.0"
    tested_version: "1.27.0"
    confidence: verified
code_blocks:
  - id: "example-mcp"
    type: executable
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-07-tool-use-mcp-tool.json)

# MCP Tool

**Category:** `tool-use`  
**Skill Level:** `intermediate`  
**Stability:** `stable`
**Added:** 2025-03

### Description

Expose tools via the Model Context Protocol (MCP), enabling any MCP-compatible client (Claude Desktop, Cursor, custom agents) to call your tools.

### Example

```python
# pip install mcp
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("my-tools")

@mcp.tool()
def get_weather(city: str) -> dict:
    """Get current weather for a city."""
    # Replace with real API call
    return {"city": city, "temp_c": 22, "condition": "sunny"}

@mcp.tool()
def calculate(expression: str) -> float:
    """Safely evaluate a mathematical expression."""
    import ast, operator
    ops = {ast.Add: operator.add, ast.Sub: operator.sub,
           ast.Mult: operator.mul, ast.Div: operator.truediv}
    def eval_expr(node):
        if isinstance(node, ast.Num): return node.n
        elif isinstance(node, ast.BinOp): return ops[type(node.op)](eval_expr(node.left), eval_expr(node.right))
        raise ValueError("Unsupported expression")
    return eval_expr(ast.parse(expression, mode="eval").body)

if __name__ == "__main__":
    mcp.run()
```

### Related Skills
- `custom-api-wrapper`, `tool-selection`, `tool-guardrails`, `openai-api`
