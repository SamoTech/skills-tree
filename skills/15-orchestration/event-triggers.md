![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-15-orchestration-event-triggers.json)

**Category:** Orchestration
**Skill Level:** Advanced
**Stability:** stable
**Added:** 2025-03

### Description
Fires agent workflows in response to external events — webhook callbacks, file system changes, cron schedules, database triggers, or message queue messages. Decouples event producers from agent consumers using an event loop or serverless function.

### Example
```python
import asyncio
from dataclasses import dataclass
from typing import Callable, Any

@dataclass
class Event:
    type: str
    payload: Any

class EventBus:
    def __init__(self):
        self._handlers: dict[str, list[Callable]] = {}

    def on(self, event_type: str, handler: Callable[[Event], Any]) -> None:
        self._handlers.setdefault(event_type, []).append(handler)

    async def emit(self, event: Event) -> None:
        handlers = self._handlers.get(event.type, [])
        await asyncio.gather(*[
            handler(event) if asyncio.iscoroutinefunction(handler)
            else asyncio.to_thread(handler, event)
            for handler in handlers
        ])

bus = EventBus()

async def on_new_issue(event: Event):
    print(f"[Agent] New GitHub issue: #{event.payload['number']} — {event.payload['title']}")
    print("[Agent] Triaging and assigning labels...")

async def on_pr_merged(event: Event):
    print(f"[Agent] PR #{event.payload['number']} merged. Triggering deployment...")

bus.on("github.issues.opened", on_new_issue)
bus.on("github.pull_request.merged", on_pr_merged)

async def main():
    await bus.emit(Event("github.issues.opened", {"number": 42, "title": "Bug: login fails"}))
    await bus.emit(Event("github.pull_request.merged", {"number": 17}))

asyncio.run(main())
```

### Related Skills
- [Agent Communication](agent-communication.md)
- [Task Queue Management](task-queue.md)
- [Sequential Workflow](sequential-workflow.md)
