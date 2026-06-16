# Example: MCP Server

A Model Context Protocol server that exposes Skills Tree as tools available to Claude Desktop, Cursor, Cline, and any MCP-compatible AI host.

## Tools Exposed

| Tool | Description |
|---|---|
| `search_skills` | Semantic search across 515+ skills |
| `get_skill` | Get full skill details by ID |
| `get_prerequisites` | Get the prerequisite chain for a skill |
| `get_category` | List all skills in a category |

## Setup

```bash
pip install -r requirements.txt
```

## Run

```bash
python server.py
```

The server listens on stdio (MCP standard transport).

## Configure in Claude Desktop

Add to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "skills-tree": {
      "command": "python",
      "args": ["/path/to/examples/mcp-server/server.py"]
    }
  }
}
```

## What You Can Ask Claude

Once connected:
- *"What skills do I need to build a production RAG system?"*
- *"Show me the prerequisites for chain-of-thought reasoning"*
- *"What are the foundational skills for AI agent development?"*
