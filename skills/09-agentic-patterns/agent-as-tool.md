---
title: "Agent as Tool"
category: 09-agentic-patterns
level: intermediate
stability: stable
description: "Expose a specialised agent as a callable tool inside a parent agent's tool loop."
added: "2026-04"
version: v2
---

# Agent as Tool
Category: agentic-patterns | Level: intermediate | Stability: stable | Version: v2

## Description
In the OpenAI Agents SDK, any agent can be wrapped as a tool using `agent.as_tool()`. The parent agent calls it like a function tool — passing a string input, receiving a string output — while the child agent runs a full inner loop internally. Unlike a handoff, the parent retains control after the child finishes and can continue its own reasoning.

## Inputs
- `agent`: the child `Agent` to wrap
- `tool_name`: string name exposed to the parent LLM
- `tool_description`: natural-language description guiding when to invoke it
- `input`: free-form string passed by the parent when calling the tool

## Outputs
- String result from the child agent's final output
- Parent's `RunResult` continues with the child's output inserted as a tool response

## Example
```python
from agents import Agent, Runner

summariser = Agent(
    name="Summariser",
    instructions="Summarise the provided text in two sentences."
)

orchestrator = Agent(
    name="Orchestrator",
    instructions="Use the summarise tool when the user provides long text.",
    tools=[summariser.as_tool(tool_name="summarise", tool_description="Summarise long text")]
)

result = Runner.run_sync(orchestrator, "Summarise this article: ...")
print(result.final_output)
```

## Failure Modes
| Cause | Symptom | Mitigation |
|---|---|---|
| Parent ignores tool | Child never invoked | Strengthen `tool_description` with explicit trigger conditions |
| Child enters infinite loop | Timeout / token overflow | Set `max_turns` on child runner config |
| Output too long for tool slot | Truncated response | Instruct child to keep output under token budget |

## Prompt Patterns
**Basic:** `"Use the summarise tool whenever the input exceeds 500 words."`

**Chain-of-Thought:** `"First assess input length, then decide whether the summarise tool is needed."`

**Constrained Output:** `"Return only the tool call. Do not paraphrase the result yourself."`

## Model Comparison
| Capability | GPT-4o | Claude 3.7 Sonnet | Gemini 2.0 Flash |
|---|---|---|---|
| Tool selection accuracy | ✅ High | ✅ High | ⚠️ Moderate |
| Output quality from child | ✅ Strong | ✅ Strong | ✅ Good |
| Latency (nested loops) | High | Moderate-High | Moderate |
| Cost efficiency | Low | Moderate | High |
| Instruction adherence | ✅ Reliable | ✅ Reliable | ⚠️ Variable |

## Related
- `agent-handoffs.md` · `subagent-delegation.md` · `tool-use-loop.md` · `specialist-agent-routing.md`

## Changelog
- v2 (2026-04): Full expansion with I/O, example, failure modes, prompt patterns, model comparison
