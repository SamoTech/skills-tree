# MCP (Model Context Protocol)

**Category:** `tool-use`  
**Skill Level:** `advanced`  
**Stability:** `stable`

### Description

Connect AI agents to any external tool, data source, or service via the open Model Context Protocol standard. MCP servers expose tools, resources, and prompts that any MCP-compatible client can consume.

### Architecture

```
Agent (MCP Client)
  │
  ├── MCP Server: GitHub  → repos, issues, PRs
  ├── MCP Server: Filesystem → read/write files
  ├── MCP Server: Playwright → browser control
  └── MCP Server: Custom API → any REST service
```

### Example

```json
// mcp_servers.json
{
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": { "GITHUB_PERSONAL_ACCESS_TOKEN": "..." }
    }
  }
}
```

### Related Skills

- [Function Calling](function-calling.md)
- [A2A Tool](a2a-tool.md)
- [Browser Tool](browser-tool.md)
