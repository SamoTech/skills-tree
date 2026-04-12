# Subagent Spawning

**Category:** `orchestration`  
**Skill Level:** `advanced`  
**Stability:** `stable`
**Added:** 2025-03

### Description

Dynamically create and manage child agent instances to handle delegated sub-tasks in parallel or sequence.

### Example

```python
# LangGraph subgraph delegation
builder = StateGraph(State)
builder.add_node('orchestrator', orchestrator_node)
builder.add_node('researcher', researcher_agent)
builder.add_node('writer', writer_agent)
builder.add_edge('orchestrator', 'researcher')
builder.add_edge('researcher', 'writer')
```

### Frameworks

- LangGraph
- AutoGen
- CrewAI
- MetaGPT

### Related Skills

- [Parallel Task Execution](parallel-execution.md)
- [Agent Handoff](agent-handoff.md)
- [Role Assignment](role-assignment.md)
