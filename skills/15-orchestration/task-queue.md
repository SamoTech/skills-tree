---
title: "Task Queue"
category: 15-orchestration
level: advanced
stability: stable
description: "Apply task queue in AI agent workflows."
added: "2025-03"
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-15-orchestration-task-queue.json)

**Category:** Orchestration
**Skill Level:** Advanced
**Stability:** stable
**Added:** 2025-03

### Description
Manages an ordered priority queue of pending agent tasks with support for task priorities, deduplication, dead-letter queuing for failed tasks, and worker pool consumption. Integrates with Redis Queue (RQ), Celery, or a lightweight in-process implementation.

### Example
```python
import heapq
import threading
from dataclasses import dataclass, field
from typing import Any, Callable

@dataclass(order=True)
class Task:
    priority: int
    task_id: str = field(compare=False)
    fn: Callable = field(compare=False)
    args: tuple = field(compare=False, default_factory=tuple)

class TaskQueue:
    def __init__(self):
        self._heap: list[Task] = []
        self._lock = threading.Lock()
        self.failed: list[Task] = []

    def enqueue(self, task: Task) -> None:
        with self._lock:
            heapq.heappush(self._heap, task)

    def process_next(self) -> bool:
        with self._lock:
            if not self._heap:
                return False
            task = heapq.heappop(self._heap)
        try:
            task.fn(*task.args)
        except Exception as e:
            print(f"Task {task.task_id} failed: {e}")
            self.failed.append(task)
        return True

queue = TaskQueue()
queue.enqueue(Task(priority=2, task_id="low",  fn=print, args=("Low priority task",)))
queue.enqueue(Task(priority=0, task_id="high", fn=print, args=("High priority task",)))
queue.process_next()   # High priority task
queue.process_next()   # Low priority task
```

### Related Skills
- [Parallel Task Execution](parallel-execution.md)
- [Sequential Workflow](sequential-workflow.md)
- [Retry with Backoff](retry-backoff.md)
