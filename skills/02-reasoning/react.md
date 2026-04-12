# ReAct (Reasoning + Acting)

**Category:** `reasoning`  
**Skill Level:** `intermediate`  
**Stability:** `stable`

### Description

Interleaves reasoning (Thought) steps with action (Act) steps and observation (Obs) steps in a loop until a task is complete. The most widely used agentic reasoning pattern.

### Example

```
Thought: I need to find the population of Cairo.
Action: web_search("Cairo population 2025")
Observation: Cairo has approximately 22 million people.
Thought: I now have the answer.
Final Answer: Cairo's population is approximately 22 million.
```

### Frameworks

- LangChain `AgentExecutor`
- LangGraph `create_react_agent`
- OpenAI Assistants API
- Pydantic AI

### Related Skills

- [Chain of Thought](chain-of-thought.md)
- [Tool-Use Loop](../09-agentic-patterns/tool-use-loop.md)
- [Planning](planning.md)
