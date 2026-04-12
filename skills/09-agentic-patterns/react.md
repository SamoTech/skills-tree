# ReAct (Reasoning + Acting)

**Category:** `agentic-patterns`
**Skill Level:** `intermediate`
**Stability:** `stable`
**Added:** 2025-03

### Description

Interleaves Thought → Action → Observation steps in a loop until the task is complete. The most widely used agentic reasoning pattern.

### Example

```
Thought: I need to find Cairo's population.
Action: web_search("Cairo population 2025")
Observation: Cairo has ~22 million people.
Thought: I now have the answer.
Final Answer: Cairo's population is approximately 22 million.
```

### Frameworks

- LangChain `AgentExecutor`
- LangGraph `create_react_agent`
- OpenAI Assistants API
- Pydantic AI

### Related Skills

- [Chain of Thought](cot.md)
- [Tool-Use Loop](tool-use-loop.md)
- [Planning](../02-reasoning/planning.md)
