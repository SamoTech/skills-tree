---
title: "Output Guardrails"
category: 14-security
level: intermediate
stability: stable
description: "Validate an agent's final response before returning it to the user."
added: "2026-04"
version: v2
---

# Output Guardrails
Category: security | Level: intermediate | Stability: stable | Version: v2

## Description
Output guardrails run after the main agent produces its final response but before the result is returned to the caller. They use `@output_guardrail` in the OpenAI Agents SDK and can block responses that contain PII, competitor mentions, harmful content, or schema violations. They are the last line of defence before the user sees a response.

## Inputs
- `agent_output`: the final string or structured response from the main agent
- `guardrail_function`: async function decorated with `@output_guardrail`
- `RunContext`: shared state

## Outputs
- Pass: `RunResult` returned to caller unchanged
- Fail: `OutputGuardrailTripwireTriggered` exception with diagnostic payload

## Example
```python
from agents import output_guardrail, GuardrailFunctionOutput, RunContextWrapper, Agent
from pydantic import BaseModel

class PIICheck(BaseModel):
    contains_pii: bool

@output_guardrail
async def pii_filter(ctx: RunContextWrapper, agent: Agent, output: str):
    import re
    has_pii = bool(re.search(r'\b\d{3}-\d{2}-\d{4}\b', output))  # SSN pattern
    return GuardrailFunctionOutput(tripwire_triggered=has_pii)

agent = Agent(
    name="DataAgent",
    instructions="Answer data questions.",
    output_guardrails=[pii_filter]
)
```

## Failure Modes
| Cause | Symptom | Mitigation |
|---|---|---|
| Regex too narrow | PII in different formats slips through | Combine regex with LLM-based PII classifier |
| Guardrail adds high latency | Slow responses | Use fast model or async parallel validation |
| False positives on code snippets | Valid code blocked | Exempt code blocks from PII scan |

## Prompt Patterns
**Basic:** `"Does this response contain any personally identifiable information?"`

**Chain-of-Thought:** `"Scan for names, emails, phone numbers, SSNs, and addresses before deciding."`

**Constrained Output:** `"Output only {contains_pii: bool, pii_types: list[str]}."`

## Model Comparison
| Capability | GPT-4o | Claude 3.7 Sonnet | Gemini 2.0 Flash |
|---|---|---|---|
| PII detection accuracy | ✅ High | ✅ Very High | ⚠️ Moderate |
| Latency | Moderate | Moderate | Low |
| Schema compliance | ✅ Strong | ✅ Strong | ⚠️ Variable |
| False positive rate | Low | Very Low | Moderate |
| Cost | Moderate | Moderate | Low |

## Related
- `input-guardrails.md` · `tool-guardrails.md` · `tool-permission-scoping.md`

## Changelog
- v2 (2026-04): Full expansion
