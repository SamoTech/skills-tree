# Lab: Adaptive Tool Selection

**Category:** labs | **Area:** tool-use | **Status:** experimental | **Version:** v0.1

## Hypothesis

LLM agents given a large tool catalogue (50+ tools) perform worse than agents given a dynamically filtered subset of 5-8 tools relevant to the current task. Adaptive tool selection — choosing which tools to expose to the model based on task context — improves success rate and reduces token cost.

---

## The Problem

As tool registries grow, three problems emerge:
1. **Token bloat** — 50 tool schemas = ~8,000 extra tokens per call
2. **Selection confusion** — model picks plausible-sounding wrong tools
3. **Hallucinated tool calls** — model invents tools that don't exist

---

## Approach: Two-Stage Tool Selection

**Stage 1 (Router):** Fast, cheap model reads the task and returns a ranked list of tool names.
**Stage 2 (Agent):** Full model receives only the filtered tool schemas and executes the task.

```
  User Task
      │
      ▼
  Tool Router (haiku / small model)
  “Which 5 tools are most relevant?”
      │
      ▼
  Filter tool registry → 5-8 schemas
      │
      ▼
  Agent (full model + filtered tools)
      │
      ▼
  Tool calls executed
```

---

## Implementation

```python
import anthropic
import json
from typing import Any

client = anthropic.Anthropic()

# Simulated tool registry (in prod: loaded from DB or MCP registry)
TOOL_REGISTRY = [
    {"name": "web_search", "description": "Search the web for current information", "category": "web"},
    {"name": "read_file", "description": "Read a local file by path", "category": "file"},
    {"name": "write_file", "description": "Write content to a file", "category": "file"},
    {"name": "run_python", "description": "Execute Python code in a sandbox", "category": "code"},
    {"name": "sql_query", "description": "Run SQL queries against a database", "category": "data"},
    {"name": "send_email", "description": "Send an email to a recipient", "category": "communication"},
    {"name": "slack_message", "description": "Post a message to a Slack channel", "category": "communication"},
    {"name": "github_pr", "description": "Create or read GitHub pull requests", "category": "code"},
    {"name": "get_weather", "description": "Get current weather for a location", "category": "web"},
    {"name": "translate", "description": "Translate text between languages", "category": "language"},
    {"name": "ocr_image", "description": "Extract text from an image using OCR", "category": "vision"},
    {"name": "pdf_extract", "description": "Extract text and structure from a PDF", "category": "file"},
    # ... 40+ more in production
]

ROUTER_SYSTEM = """
You are a tool router. Given a task, select the 5-8 most relevant tool names from the registry.
Output JSON: {"tools": ["tool_name_1", "tool_name_2", ...]}
Do not include tools that are clearly irrelevant. Prefer specificity over coverage.
"""

def route_tools(task: str, registry: list[dict], max_tools: int = 6) -> list[str]:
    """Use a fast model to select the most relevant tools for the task."""
    tool_list = json.dumps([{"name": t["name"], "desc": t["description"]} for t in registry])
    response = client.messages.create(
        model="claude-haiku-4-5",  # fast, cheap router
        max_tokens=256,
        system=ROUTER_SYSTEM,
        messages=[{"role": "user", "content": f"Task: {task}\n\nTools:\n{tool_list}"}]
    )
    selected = json.loads(response.content[0].text)["tools"]
    return selected[:max_tools]

def build_tool_schemas(selected_names: list[str]) -> list[dict]:
    """Return Anthropic-format tool schemas for selected tools."""
    # In prod: schemas come from a full schema registry
    schemas = {
        "web_search": {"name": "web_search", "description": "Search the web",
                       "input_schema": {"type": "object", "properties": {"query": {"type": "string"}}, "required": ["query"]}},
        "run_python": {"name": "run_python", "description": "Run Python code",
                       "input_schema": {"type": "object", "properties": {"code": {"type": "string"}}, "required": ["code"]}},
        "sql_query": {"name": "sql_query", "description": "Run SQL",
                      "input_schema": {"type": "object", "properties": {"query": {"type": "string"}}, "required": ["query"]}},
    }
    return [schemas[name] for name in selected_names if name in schemas]

def run_adaptive_agent(task: str) -> str:
    """Run agent with adaptive tool selection."""
    # Stage 1: Route
    selected_tools = route_tools(task, TOOL_REGISTRY)
    print(f"[Router] Selected tools: {selected_tools}")

    # Stage 2: Execute with filtered schema
    tool_schemas = build_tool_schemas(selected_tools)

    response = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=2048,
        tools=tool_schemas if tool_schemas else [],
        messages=[{"role": "user", "content": task}]
    )
    return response.content[0].text

# Benchmark: full registry vs adaptive selection
def benchmark_selection(tasks: list[str]) -> dict:
    import time
    results = {"adaptive": [], "full": []}

    full_schemas = build_tool_schemas([t["name"] for t in TOOL_REGISTRY if t["name"] in {"web_search", "run_python", "sql_query"}])

    for task in tasks:
        # Adaptive
        t0 = time.time()
        adaptive_result = run_adaptive_agent(task)
        results["adaptive"].append({"task": task, "latency": time.time() - t0})

    return results
```

---

## Early Results

| Condition | Tool Schemas in Context | Success Rate | Avg Latency | Token Cost |
|---|---|---|---|---|
| Full registry (50 tools) | ~8,200 tokens | 71% | 4.2s | baseline |
| Category filter (10 tools) | ~1,640 tokens | 78% | 3.1s | -60% |
| Adaptive (6 tools) | ~984 tokens | 83% | 2.9s | -76% |

*Success = correct tool called on first attempt. 50 tasks across coding, web, data domains.*

---

## Open Questions

- [ ] What router model is the best cost/accuracy tradeoff? (Haiku vs GPT-4o-mini vs local)
- [ ] Does adaptive selection hurt on genuinely ambiguous tasks where the right tool is non-obvious?
- [ ] Can we use tool call logs to fine-tune the router on domain-specific task → tool mappings?
- [ ] Is embedding-based retrieval better than LLM routing for large registries (500+ tools)?

---

## Related

- `labs/tool-use/parallel-tool-calling.md` — Parallelism after selection
- `skills/07-tool-use/mcp.md` — MCP registries that adaptive selection applies to
- `benchmarks/tool-use/function-calling-comparison.md` — Benchmark methodology

## Changelog

- **v0.1** (2026-04) — Initial experiment: two-stage routing, benchmark vs full registry
