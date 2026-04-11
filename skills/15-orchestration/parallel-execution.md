# Parallel Task Execution

**Category:** `orchestration`  
**Skill Level:** `advanced`  
**Stability:** `stable`

### Description

Run multiple independent agent tasks concurrently to reduce total wall-clock time.

### Example

```python
import asyncio

async def run_all():
    results = await asyncio.gather(
        agent.run('Summarize document A'),
        agent.run('Summarize document B'),
        agent.run('Summarize document C'),
    )
    return results
```

### Frameworks

- LangGraph parallel nodes
- AutoGen group chat
- Python `asyncio`

### Related Skills

- [Subagent Spawning](subagent-spawning.md)
- [Sequential Workflow](sequential-workflow.md)
