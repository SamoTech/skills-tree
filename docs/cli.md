# CLI Reference

Skills Tree ships with a command-line interface built with [Typer](https://typer.tiangolo.com/).

## Installation

```bash
pip install skills-tree
```

## Commands

### `skills-tree search`

Search for skills by keyword.

```bash
skills-tree search "memory injection"
skills-tree search "rag" --limit 10
skills-tree search "web" --category web
```

**Options:**

| Option | Description | Default |
|---|---|---|
| `--limit` | Maximum results to return | 20 |
| `--category` | Filter by category ID | None |
| `--level` | Filter by level (beginner/intermediate/advanced) | None |
| `--badge` | Filter by badge (verified/reviewed/stub) | None |

---

### `skills-tree show`

Display the full specification of a skill.

```bash
skills-tree show rag
skills-tree show memory-injection --format json
```

**Options:**

| Option | Description | Default |
|---|---|---|
| `--format` | Output format: `text`, `json`, `yaml` | `text` |

---

### `skills-tree list`

List skills, optionally filtered.

```bash
skills-tree list
skills-tree list --category reasoning
skills-tree list --badge verified
```

---

### `skills-tree categories`

List all 17 skill categories.

```bash
skills-tree categories
```

---

### `skills-tree mcp serve`

Start the MCP server for agent-to-agent capability discovery.

```bash
skills-tree mcp serve
skills-tree mcp serve --port 8080 --host 0.0.0.0
```

**Options:**

| Option | Description | Default |
|---|---|---|
| `--port` | Port to listen on | 8000 |
| `--host` | Host to bind to | `127.0.0.1` |

---

### `skills-tree --version`

Print the installed version.

```bash
skills-tree --version
```
