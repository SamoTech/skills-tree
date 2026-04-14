---
title: "Multi-Agent Run Config"
category: 15-orchestration
level: intermediate
stability: stable
description: "Configure Runner settings — max turns, hooks, tracing, and context — for multi-agent runs in the OpenAI Agents SDK."
added: "2026-04"
version: v2
---

# Multi-Agent Run Config
Category: orchestration | Level: intermediate | Stability: stable | Version: v2

## Description
`RunConfig` in the OpenAI Agents SDK controls how a multi-agent run executes: maximum turn count, model override, tracing settings, input/output guardrails at the run level, and lifecycle hooks. Setting `max_turns` prevents runaway loops; hooks let you log or modify behaviour at each agent step without changing agent code.

## Inputs
- `max_turns`: integer cap on agent-model round trips (default: 10)
- `model`: optional model override for all agents in the run
- `tracing_disabled`: bool, disables OpenAI trace collection
- `hooks`: `RunHooks` instance with `on_agent_start`, `on_tool_call`, `on_agent_end` callbacks
- `context`: typed context object shared across all agents

## Outputs
- `RunResult` containing `final_output`, `all_messages`, and per-agent traces

## Example
```python
from agents import Agent, Runner, RunConfig, RunHooks

class LogHooks(RunHooks):
    async def on_agent_start(self, ctx, agent):
        print(f"Agent started: {agent.name}")

config = RunConfig(max_turns=5, hooks=LogHooks())
result = Runner.run_sync(triage_agent, "Help me with billing.", run_config=config)
```

## Failure Modes
| Cause | Symptom | Mitigation |
|---|---|---|
| `max_turns` too low | Run truncated before task complete | Profile typical task depth and set `max_turns` with 2× buffer |
| Hook raises exception | Entire run fails | Wrap hook body in try/except and log errors |
| Model override breaks tool schema | Tool calls fail | Verify target model supports all tools used by agents |

## Prompt Patterns
**Basic:** `"Set max_turns=10 for most production runs."`

**Chain-of-Thought:** `"Estimate the number of tool calls a task requires and add 3 turns as buffer."`

**Constrained Output:** `"Use RunConfig hooks for logging only; avoid mutating agent state inside hooks."`

## Model Comparison
| Capability | GPT-4o | Claude 3.7 Sonnet | Gemini 2.0 Flash |
|---|---|---|---|
| Multi-turn stability | ✅ High | ✅ High | ⚠️ Moderate |
| Tool schema compatibility | ✅ Full | ✅ Full | ⚠️ Some gaps |
| Hook latency impact | Minimal | Minimal | Minimal |
| Cost at max_turns=10 | High | Moderate | Low |
| Trace quality | ✅ Rich | ⚠️ SDK-dependent | ⚠️ Limited |

## Related
- `agent-handoffs.md` · `specialist-agent-routing.md` · `human-approval-gates.md` · `stateful-agent-graphs.md`

## Changelog
- v2 (2026-04): Full expansion
