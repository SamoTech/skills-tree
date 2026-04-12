# Tool-Use Loop

**Category:** `agentic-patterns`
**Skill Level:** `intermediate`
**Stability:** `stable`
**Added:** 2025-03

### Description

The agent iteratively calls tools (functions, APIs, search) and processes their results until the task is complete or a stop condition is reached.

### Example

```
Loop iteration 1:
  → call weather_api(city="Cairo")
  ← {"temp": 32, "condition": "sunny"}

Loop iteration 2:
  → call translate(text="sunny", target="Arabic")
  ← "مشمس"

Stop condition: all required data collected.
Final answer: "القاهرة 32 درجة ومشمس"
```

### Related Skills

- [ReAct](react.md)
- [MCP Tool](../07-tool-use/mcp-tool.md)
- [Plan and Execute](plan-and-execute.md)
