---
title: "MCP Tool Use"
category: 07-tool-use
level: intermediate
stability: stable
description: "Apply mcp tool in AI agent workflows."
---


![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-07-tool-use-mcp-tool.json)

# MCP Tool Use

### Description
Interacts with Model Context Protocol (MCP) servers to access tools, resources, and prompts exposed by external services. MCP provides a standardized JSON-RPC interface for LLM tool integration, enabling agents to discover available tools at runtime, invoke them with typed parameters, and handle streaming responses.

### When to Use
- Integrating with MCP-compatible services (GitHub MCP, filesystem MCP, browser MCP, etc.)
- Building agents that discover and use tools dynamically without hardcoded wrappers
- Exposing custom tools to Claude via MCP server implementations
- Multi-tool orchestration where tools are discovered from multiple MCP servers

### Example
```python
# MCP Client using the official Python SDK
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
import asyncio

async def use_mcp_tools(server_command: list[str], tool_name: str, args: dict):
    server_params = StdioServerParameters(command=server_command[0], args=server_command[1:])
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            # Discover available tools
            tools = await session.list_tools()
            print(f"Available tools: {[t.name for t in tools.tools]}")

            # Call a specific tool
            result = await session.call_tool(tool_name, arguments=args)
            return result.content

# Example: use filesystem MCP server
result = asyncio.run(use_mcp_tools(
    ["npx", "-y", "@modelcontextprotocol/server-filesystem", "/tmp"],
    "read_file",
    {"path": "/tmp/example.txt"}
))
print(result)
```

### Advanced Techniques
- **Multi-server orchestration**: initialize multiple MCP sessions and route tool calls based on tool name prefix
- **Dynamic tool discovery**: call `list_tools()` at agent startup and inject schema into the system prompt automatically
- **Resource streaming**: use `read_resource()` with URI templates to stream large files from MCP servers
- **Custom MCP server**: implement `@server.call_tool()` handlers with `mcp.server.fastmcp.FastMCP`

### Related Skills
- `api-tool`, `tool-use-loop`, `a2a-tool`, `subagent-delegation`, `bash-tool`
