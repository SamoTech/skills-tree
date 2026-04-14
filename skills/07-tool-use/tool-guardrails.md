---
title: "Tool Guardrails"
category: 07-tool-use
level: intermediate
stability: stable
description: "Validate agent inputs and outputs with lightweight guardrail agents before executing or returning tool results."
added: "2026-04"
version: v2
---

# Tool Guardrails
Category: tool-use | Level: intermediate | Stability: stable | Version: v2

## Description
In the OpenAI Agents SDK, guardrails are lightweight validation agents that run in parallel with the main agent. Input guardrails inspect the user message before the agent processes it; output guardrails inspect the agent's response before it is returned. Guardrails raise `InputGuardrailTripwireTriggered` or `OutputGuardrailTripwireTriggered` exceptions to halt execution. They apply to function tools; built-in hosted tools and handoffs use separate safety mechanisms.

## Inputs
- `guardrail_function`: async function decorated with `@input_guardrail` or `@output_guardrail`
- `context`: `RunContext` available inside the guardrail
- `agent`: the parent `Agent` the guardrail is attached to
- `input` / `output`: message or response being validated

## Outputs
- `GuardrailFunctionOutput(tripwire_triggered=False)` — execution continues
- `GuardrailFunctionOutput(tripwire_triggered=True)` — exception raised, run halted

## Example
```python
from agents import Agent, Runner, input_guardrail, GuardrailFunctionOutput, RunContextWrapper
from pydantic import BaseModel

class SafetyCheck(BaseModel):
    is_harmful: bool
    reason: str

@input_guardrail
async def harm_check(ctx: RunContextWrapper, agent: Agent, input: str) -> GuardrailFunctionOutput:
    result = await Runner.run(safety_agent, input, context=ctx.context)
    output = result.final_output_as(SafetyCheck)
    return GuardrailFunctionOutput(output_info=output, tripwire_triggered=output.is_harmful)

main_agent = Agent(
    name="Assistant",
    instructions="Be helpful.",
    input_guardrails=[harm_check]
)
```

## Failure Modes
| Cause | Symptom | Mitigation |
|---|---|---|
| Guardrail agent too slow | High latency on every turn | Use a fast small model (e.g. gpt-4o-mini) for the guardrail |
| Over-sensitive tripwire | Legitimate inputs blocked | Tune guardrail prompt with explicit examples of safe content |
| Guardrail misses edge case | Harmful output slips through | Layer multiple guardrails or add output guardrail as backup |

## Prompt Patterns
**Basic:** `"Classify the following input as harmful or safe. Output JSON with is_harmful and reason."`

**Chain-of-Thought:** `"Think through potential harms step by step before classifying."`

**Constrained Output:** `"Respond ONLY with valid JSON matching {is_harmful: bool, reason: string}."`

## Model Comparison
| Capability | GPT-4o | Claude 3.7 Sonnet | Gemini 2.0 Flash |
|---|---|---|---|
| Classification accuracy | ✅ High | ✅ Very High | ⚠️ Moderate |
| Latency as guardrail | Moderate | Moderate | Low |
| JSON output reliability | ✅ Strong | ✅ Strong | ⚠️ Occasional schema drift |
| Cost per check | Moderate | Moderate | Low |
| Edge-case coverage | ✅ Good | ✅ Strong | ⚠️ Limited |

## Related
- `input-guardrails.md` · `output-guardrails.md` · `tool-permission-scoping.md` · `approval-before-destructive-tools.md`

## Changelog
- v2 (2026-04): Full expansion with I/O, example, failure modes, prompt patterns, model comparison
