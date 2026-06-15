# Architect MCP Server v1

Sprint: **C-10**

Architect is now exposed as an MCP (Model Context Protocol) server so external AI clients such as Claude Desktop, Cursor, and VS Code can call live Skills Tree recommendations and blueprint generation.

---

## Architecture

MCP Server v1 uses the **existing API layer** introduced in Sprint C-09. This avoids business-logic duplication and preserves a single execution path.

```text
Claude Desktop / Cursor / VS Code
            │
            ▼
      mcp/server.py
            │
            ▼
       mcp/tools.py
            │
            ▼
        api.main app
            │
            ▼
  FastAPI route handlers (/recommend, /blueprint, /goals, /skills)
            │
            ▼
GoalTaxonomyParser / SkillsGraph / RecommendationEngine / BlueprintGenerator
```

### Design Principles

- **No duplicated logic** — MCP tools call the existing API layer.
- **Live recommendations** — `recommend_skills()` returns the same calibrated response as `POST /recommend`.
- **Transport simplicity** — stdio JSON-RPC 2.0 for local desktop client compatibility.
- **Single source of truth** — taxonomy, graph, calibration, and blueprint logic remain in the engine and API layers.

---

## Tool Contracts

### `recommend_skills`

Returns live Architect recommendations for a goal.

**Input**

```json
{
  "goal": "Coding Agent",
  "experience": "intermediate",
  "time_budget_hours": 80
}
```

**Output**

```json
{
  "goal": "Coding Agent",
  "goal_id": "G01",
  "confidence_score": 0.86,
  "required_skills": [ ... ],
  "optional_skills": [ ... ],
  "learning_path": [ ... ],
  "deployment": "cloud",
  "complexity": "Intermediate",
  "estimated_learn_hours": 96,
  "calibration_applied": true
}
```

---

### `generate_blueprint`

Generates a full architecture blueprint JSON using `BlueprintGenerator`.

**Input**

```json
{
  "goal": "Coding Agent"
}
```

**Output**

```json
{
  "id": "blueprint-20260615143000",
  "title": "Coding Agent",
  "goal": "Coding Agent",
  "goal_id": "G01",
  "confidence_score": 0.86,
  "architecture_type": "Single-Agent",
  "required_skills": [ ... ],
  "optional_skills": [ ... ],
  "learning_path": [ ... ],
  "risks": [ ... ]
}
```

---

### `list_goals`

Returns all taxonomy goals.

**Input**

```json
{}
```

**Output**

```json
[
  {"id": "G01", "name": "Coding Agent"},
  {"id": "G02", "name": "Browser Agent"}
]
```

---

### `list_skills`

Returns all skill nodes from the graph.

**Input**

```json
{}
```

**Output**

```json
[
  {"id": "skill:code-generation", "name": "Code Generation"},
  {"id": "skill:rag-retrieval", "name": "RAG Retrieval"}
]
```

---

## Examples

### Example 1 — Claude asks for a coding agent

**Tool call**

```json
{
  "name": "recommend_skills",
  "arguments": {
    "goal": "Coding Agent",
    "experience": "intermediate",
    "time_budget_hours": 80
  }
}
```

### Example 2 — Generate a RAG blueprint

**Tool call**

```json
{
  "name": "generate_blueprint",
  "arguments": {
    "goal": "RAG Assistant"
  }
}
```

### Example 3 — Explore taxonomy goals

**Tool call**

```json
{
  "name": "list_goals",
  "arguments": {}
}
```

---

## Running Locally

From the repository root:

```bash
python -m mcp.server
```

or:

```bash
python mcp/server.py
```

---

## Claude Desktop Configuration

Add this to Claude Desktop MCP config:

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

### Windows example

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

---

## Cursor Configuration

Add to Cursor MCP settings:

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

---

## VS Code Configuration

Example VS Code MCP / agent-tools style configuration:

```json
{
  "servers": {
    "skills-tree-architect": {
      "type": "stdio",
      "command": "python",
      "args": ["-m", "mcp.server"],
      "cwd": "/absolute/path/to/skills-tree"
    }
  }
}
```

---

## Validation

Run the MCP test suite:

```bash
pytest tests/test_mcp.py -v
```

Coverage includes:

- tool metadata
- direct tool calls
- dispatcher behavior
- JSON-RPC request handling
- success and failure paths

---

## Success Criteria

Claude Desktop can call:

```text
recommend_skills()
```

and receive live Architect recommendations because the MCP server routes the request through the existing API and engine stack.
