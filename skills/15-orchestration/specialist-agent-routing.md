---
title: "Specialist Agent Routing"
category: 15-orchestration
level: intermediate
stability: stable
description: "Route incoming requests to the correct specialist agent based on intent classification."
added: "2026-04"
version: v2
---

# Specialist Agent Routing
Category: orchestration | Level: intermediate | Stability: stable | Version: v2

## Description
Specialist routing uses a triage/orchestrator agent to classify user intent and dispatch to the best-suited specialist. In the OpenAI Agents SDK this is implemented with `handoffs=[specialist_a, specialist_b, ...]` and clear `handoff_description` strings on each specialist so the LLM can make an accurate routing decision. In LangGraph it is a conditional edge on an intent-classification node.

## Inputs
- `user_input`: raw user message
- `specialists`: list of `Agent` objects with descriptive `handoff_description`
- `triage_instructions`: system prompt guiding routing logic

## Outputs
- `RunResult` from the selected specialist agent
- Routing decision visible in trace/messages

## Example
```python
from agents import Agent, Runner

support = Agent(name="Support", instructions="Handle product support.",
                handoff_description="Technical issues, bugs, how-to questions")
sales   = Agent(name="Sales",   instructions="Handle pricing and upgrades.",
                handoff_description="Pricing, plans, upgrades, renewals")

triage = Agent(
    name="Triage",
    instructions="Classify the user request and route to the right team.",
    handoffs=[support, sales]
)

result = Runner.run_sync(triage, "How much does the Pro plan cost?")
print(result.final_output)
```

## Failure Modes
| Cause | Symptom | Mitigation |
|---|---|---|
| Ambiguous `handoff_description` | Wrong specialist selected | Use mutually exclusive, concrete descriptions with examples |
| Triage agent answers instead of routing | No handoff triggered | Instruct triage explicitly: "Do not answer; only route." |
| Specialist not available | Handoff fails | Add fallback `default_agent` for unclassified intents |

## Prompt Patterns
**Basic:** `"Route this query to Support or Sales based on intent."`

**Chain-of-Thought:** `"Identify the primary need (support vs commercial), then select the matching specialist."`

**Constrained Output:** `"Output only a handoff action. Do not write a response."`

## Model Comparison
| Capability | GPT-4o | Claude 3.7 Sonnet | Gemini 2.0 Flash |
|---|---|---|---|
| Intent classification accuracy | ✅ High | ✅ High | ⚠️ Moderate |
| Ambiguity handling | ✅ Good | ✅ Good | ⚠️ Defaults to first option |
| Instruction following | ✅ Reliable | ✅ Reliable | ⚠️ Occasional miss |
| Latency | Moderate | Moderate | Low |
| Cost | Moderate | Moderate | Low |

## Related
- `agent-handoffs.md` · `multi-agent-run-config.md` · `subagent-delegation.md` · `stateful-agent-graphs.md`

## Changelog
- v2 (2026-04): Full expansion
