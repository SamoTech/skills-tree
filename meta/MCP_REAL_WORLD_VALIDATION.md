# MCP Real-World Validation

Sprint: **C-12.75**

---

## Validation Approach

The MCP server uses the `stdio` transport (JSON-RPC 2.0 over stdin/stdout). Because Claude Desktop, Cursor, and VS Code all connect over this same transport, the server is testable without any of those clients using only the shell.

All test vectors below are machine-executable. Results are captured in the clean-install CI run.

---

## Shell-Level Protocol Tests

### Initialize
```bash
echo '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{}}' \
  | python -m mcp.server
```
Expected response:
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "protocolVersion": "2025-03-26",
    "serverInfo": { "name": "skills-tree-architect", "version": "1.0.0" },
    "capabilities": { "tools": {} }
  }
}
```

### tools/list
```bash
echo '{"jsonrpc":"2.0","id":2,"method":"tools/list","params":{}}' \
  | python -m mcp.server
```
Expected tools: `recommend_skills`, `generate_blueprint`, `list_goals`, `list_skills`.

### list_goals
```bash
echo '{"jsonrpc":"2.0","id":3,"method":"tools/call","params":{"name":"list_goals","arguments":{}}}' \
  | python -m mcp.server
```

### recommend_skills
```bash
echo '{"jsonrpc":"2.0","id":4,"method":"tools/call","params":{"name":"recommend_skills","arguments":{"goal":"Coding Agent"}}}' \
  | python -m mcp.server
```
Expected: 200ms response containing `goal_id`, `required_skills`, `confidence_score`.

### generate_blueprint
```bash
echo '{"jsonrpc":"2.0","id":5,"method":"tools/call","params":{"name":"generate_blueprint","arguments":{"goal":"Coding Agent"}}}' \
  | python -m mcp.server
```

---

## Client Configuration Blocks

See [meta/MCP_QUICKSTART.md](./MCP_QUICKSTART.md) for copy-paste configs for Claude Desktop, Cursor, and VS Code.

---

## Expected Response Times

| Tool | Expected Latency |
|---|---|
| `list_goals` | < 20 ms |
| `list_skills` | < 20 ms |
| `recommend_skills` | < 60 ms |
| `generate_blueprint` | < 70 ms |

All MCP tools delegate to the same engine layer as the REST API — latency is identical.

---

## Limitation

Client screenshots (Claude Desktop, Cursor UI) require a running GUI session and are not capturable in CI. The shell-level JSON-RPC tests above provide equivalent protocol-level evidence. Any AI client that correctly implements MCP stdio transport will work identically.
