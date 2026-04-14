---
title: "Agent Sessions"
category: 03-memory
level: beginner
stability: stable
description: "Maintain automatic conversation history across multiple turns using OpenAI Agents SDK sessions."
added: "2026-04"
version: v2
---

# Agent Sessions
Category: memory | Level: beginner | Stability: stable | Version: v2

## Description
Agent sessions in the OpenAI Agents SDK automatically manage conversation history across multiple `Runner.run()` calls. Instead of manually appending messages, you pass a `Session` object; the SDK stores and retrieves the full turn history from a backing store. This enables stateful multi-turn conversations without application-level history management.

## Inputs
- `session`: a `Session` instance (e.g. `InMemorySession` or a persistent backend)
- `user_input`: new user message for the current turn
- `agent`: the `Agent` to run

## Outputs
- `RunResult` with `final_output` for the current turn
- Session store updated with the new turn appended

## Example
```python
from agents import Agent, Runner
from agents.memory import InMemorySession

session = InMemorySession()
agent = Agent(name="Assistant", instructions="Be helpful and remember context.")

# Turn 1
result1 = Runner.run_sync(agent, "My name is Ossama.", session=session)
print(result1.final_output)

# Turn 2 — agent remembers the name
result2 = Runner.run_sync(agent, "What is my name?", session=session)
print(result2.final_output)  # → "Your name is Ossama."
```

## Failure Modes
| Cause | Symptom | Mitigation |
|---|---|---|
| Session store not persisted | History lost on restart | Use database-backed session store for production |
| Session grows too large | Context window overflow | Implement session summarisation or sliding window |
| Wrong session passed | Agent answers from wrong conversation | Use unique session IDs per user or conversation |

## Prompt Patterns
**Basic:** `"Remember all details the user shares across turns."`

**Chain-of-Thought:** `"Before answering, review what the user has already told you in this session."`

**Constrained Output:** `"If you do not have enough session context to answer, ask a clarifying question."`

## Model Comparison
| Capability | GPT-4o | Claude 3.7 Sonnet | Gemini 2.0 Flash |
|---|---|---|---|
| Long-session coherence | ✅ Strong | ✅ Very Strong | ⚠️ Degrades past 32k tokens |
| Name/fact recall | ✅ Reliable | ✅ Reliable | ⚠️ Occasional miss |
| Context window | 128k | 200k | 1M |
| Cost per long session | High | Moderate | Low |
| Instruction following | ✅ Strong | ✅ Strong | ✅ Good |

## Related
- `cross-thread-memory.md` · `episodic-memory-replay.md` · `agent-handoffs.md` · `langgraph-checkpointing.md`

## Changelog
- v2 (2026-04): Full expansion
