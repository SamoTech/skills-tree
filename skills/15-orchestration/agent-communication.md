![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-15-orchestration-agent-communication.json)

**Category:** Orchestration
**Skill Level:** Advanced
**Stability:** stable
**Added:** 2025-03

### Description
Enables structured message passing between agents using a shared message bus or direct API calls. Implements request/response, publish/subscribe, and fire-and-forget patterns with typed message schemas and delivery guarantees.

### Example
```python
import asyncio
from dataclasses import dataclass, field
from typing import Any, Callable
from collections import defaultdict

@dataclass
class Message:
    sender: str
    topic: str
    payload: Any

class MessageBus:
    def __init__(self):
        self._subscribers: dict[str, list[Callable]] = defaultdict(list)

    def subscribe(self, topic: str, handler: Callable[[Message], Any]) -> None:
        self._subscribers[topic].append(handler)

    async def publish(self, message: Message) -> None:
        handlers = self._subscribers.get(message.topic, [])
        await asyncio.gather(*[asyncio.coroutine(h)(message) if not asyncio.iscoroutinefunction(h)
                                else h(message) for h in handlers])

bus = MessageBus()

async def researcher_agent(msg: Message):
    print(f"[Researcher] Got task: {msg.payload['query']}")
    await bus.publish(Message("researcher", "research.done", {"result": "Found 5 papers"}))

async def writer_agent(msg: Message):
    print(f"[Writer] Writing from: {msg.payload['result']}")

bus.subscribe("task.assign", researcher_agent)
bus.subscribe("research.done", writer_agent)
asyncio.run(bus.publish(Message("orchestrator", "task.assign", {"query": "LLM agents"})))
```

### Related Skills
- [Subagent Spawning](subagent-spawning.md)
- [Agent Handoff](agent-handoff.md)
- [Shared Memory / Blackboard](shared-memory.md)
