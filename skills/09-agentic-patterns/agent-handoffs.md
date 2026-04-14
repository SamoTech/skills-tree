---
title: "Agent Handoffs"
category: 09-agentic-patterns
level: intermediate
stability: stable
description: "Transfer control between specialised agents within a single OpenAI Agents SDK run."
added: "2026-04"
version: v2
---

# Agent Handoffs
Category: agentic-patterns | Level: intermediate | Stability: stable | Version: v2

## Description
Agent handoffs let one agent transfer execution to a more specialised agent mid-run without starting a new session. In the OpenAI Agents SDK a handoff is declared with `handoff()` or `handoffs=[...]` on the parent agent; the receiving agent inherits the conversation history and continues from where the parent stopped. Unlike calling an agent-as-tool, a handoff permanently shifts control — the original agent is no longer active in that run.

## Inputs
- `agent`: the source `Agent` object initiating the transfer
- `handoffs`: list of target `Agent` objects or `Handoff` descriptors
- `context`: optional `RunContext` carrying shared state
- `input`: user message or prior tool output that triggered the handoff

## Outputs
- `RunResult` from the receiving agent, including all messages produced after the handoff
- Updated conversation history spanning both agents

## Example
```python
from agents import Agent, Runner

billing_agent = Agent(
    name="Billing",
    instructions="Handle all billing and payment queries."
)

triage_agent = Agent(
    name="Triage",
    instructions="Route to the correct specialist.",
    handoffs=[billing_agent]
)

result = Runner.run_sync(triage_agent, "My invoice is wrong.")
print(result.final_output)
```

## Failure Modes
| Cause | Symptom | Mitigation |
|---|---|---|
| Circular handoff chain | Infinite loop between agents | Add `max_turns` limit on `Runner.run()` |
| Receiving agent lacks context | Repetitive clarifying questions | Pass shared `RunContext` or summarise history in instructions |
| Handoff triggered on wrong intent | Mis-routed queries | Add explicit `handoff_description` so the model selects the right target |

## Prompt Patterns
**Basic:** `"You are a triage agent. If the user mentions billing, hand off to the Billing agent."`

**Chain-of-Thought:** `"Think step-by-step about which specialist can best resolve this query, then hand off."`

**Constrained Output:** `"Respond ONLY with a handoff action. Do not answer the question yourself."`

## Model Comparison
| Capability | GPT-4o | Claude 3.7 Sonnet | Gemini 2.0 Flash |
|---|---|---|---|
| Handoff trigger accuracy | ✅ High | ✅ High | ⚠️ Moderate |
| Context preservation | ✅ Strong | ✅ Strong | ⚠️ Degrades on long history |
| Instruction following | ✅ Reliable | ✅ Reliable | ⚠️ Occasional drift |
| Latency | Moderate | Moderate | Low |
| Cost per run | High | Moderate | Low |

## Related
- `subagent-delegation.md` · `agent-as-tool.md` · `specialist-agent-routing.md` · `multi-agent-run-config.md`

## Changelog
- v2 (2026-04): Full expansion with I/O, example, failure modes, prompt patterns, model comparison
