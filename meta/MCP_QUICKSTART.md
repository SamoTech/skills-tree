# MCP Quickstart — Time to First Tool: < 5 Minutes

Sprint: **C-12**

---

## Prerequisites

```bash
git clone https://github.com/SamoTech/skills-tree
cd skills-tree
pip install -e .[dev]
```

Test that the MCP server starts:

```bash
echo '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{}}' | python -m mcp.server
# Expected: {"jsonrpc": "2.0", "id": 1, "result": {"protocolVersion": "2025-03-26", ...}}
```

---

## Claude Desktop

**Config file location:**
- macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
- Windows: `%APPDATA%\Claude\claude_desktop_config.json`

```json
{
  "mcpServers": {
    "skills-tree-architect": {
      "command": "python",
      "args": ["-m", "mcp.server"],
      "cwd": "/absolute/path/to/skills-tree"
    }
  }
}
```

**Windows:**
```json
{
  "mcpServers": {
    "skills-tree-architect": {
      "command": "py",
      "args": ["-m", "mcp.server"],
      "cwd": "C:\\projects\\skills-tree"
    }
  }
}
```

1. Save the config file
2. Restart Claude Desktop
3. Look for the 🔧 (hammer) icon in a new conversation
4. Ask Claude: *"What skills do I need to build a Coding Agent?"*

Claude will call `recommend_skills` automatically.

---

## Cursor

**Config file location:** `~/.cursor/mcp.json` (or via Cursor Settings → MCP)

```json
{
  "mcpServers": {
    "skills-tree-architect": {
      "command": "python",
      "args": ["-m", "mcp.server"],
      "cwd": "/absolute/path/to/skills-tree"
    }
  }
}
```

1. Save and reload Cursor
2. Open the Chat panel (`Cmd+L`)
3. Type: *"Use skills-tree to recommend skills for a RAG Assistant"*

---

## VS Code

**Config file location:** `.vscode/mcp.json` (project-level) or user settings

```json
{
  "servers": {
    "skills-tree-architect": {
      "type": "stdio",
      "command": "python",
      "args": ["-m", "mcp.server"],
      "cwd": "${workspaceFolder}"
    }
  }
}
```

With `cwd: "${workspaceFolder}"` you can open the `skills-tree` repo directly and the path resolves automatically.

---

## Available MCP Tools

| Tool | Description | Required input |
|---|---|---|
| `recommend_skills` | Live Architect recommendations | `goal` |
| `generate_blueprint` | Full architecture blueprint | `goal` |
| `list_goals` | All taxonomy goals | none |
| `list_skills` | All graph skills | none |

---

## Test the Server Manually

```bash
# List tools
echo '{"jsonrpc":"2.0","id":2,"method":"tools/list","params":{}}' | python -m mcp.server

# Call recommend_skills
echo '{"jsonrpc":"2.0","id":3,"method":"tools/call","params":{"name":"recommend_skills","arguments":{"goal":"Coding Agent"}}}' | python -m mcp.server
```
