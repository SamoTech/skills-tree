---
title: Customer Support Bot
category: systems
version: v1
stability: stable
skills: [memory-injection, intent-classification, response-generation, escalation, sentiment-analysis]
---

# Customer Support Bot

> Personalized support agent that injects user history into context, classifies intent, generates empathetic responses, and escalates to humans when confidence is low.

## Skills Used

| Skill | Role |
|---|---|
| `skills/03-memory/memory-injection.md` | Load user profile + past tickets |
| `skills/09-agentic-patterns/intent-classification.md` | Route to correct handler |
| `skills/06-communication/response-generation.md` | Draft empathetic, on-brand replies |
| `skills/02-reasoning/risk-assessment.md` | Decide when to escalate to human |
| `skills/06-communication/tone-adaptation.md` | Match urgency and sentiment of user |

## Architecture

```
User message
      │
      ▼
┌──────────────────┐
│  Memory Loader   │  top-5 past tickets + user profile from vector DB
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│ Intent Classifier│  billing / bug / howto / complaint / other
└────────┬─────────┘
    ┌────┴──────────────┬──────────────┐
    ▼                   ▼              ▼
  FAQ lookup       KB article      Free-form
  (exact match)    (RAG search)    generation
    └────────────────────┴──────────────┘
                         │
                         ▼
                 Confidence Gate
                 ≥ 0.8 → send reply
                 < 0.8 → escalate to human queue
                         │
                         ▼
                 Tone Adapter
              (mirror user sentiment)
                         │
                         ▼
                  Final response
```

## Implementation

```python
import anthropic

client = anthropic.Anthropic()

SUPPORT_SYSTEM = """
You are a customer support agent for a SaaS product.
You have been given the user's recent ticket history and profile.
Rules:
- Be empathetic and concise (≤ 120 words)
- If you are less than 80% confident in your answer, end with: ESCALATE
- Never make up feature capabilities
- Mirror the user's tone (frustrated → calm; happy → warm)
"""

def build_memory_context(user_id: str, memory_store) -> str:
    memories = memory_store.search(user_id, top_k=5)
    return "\n".join(f"- {m['date']}: {m['summary']}" for m in memories)

def handle_message(user_id: str, message: str, memory_store, kb_search) -> dict:
    memory_ctx = build_memory_context(user_id, memory_store)
    kb_results = kb_search(message, top_k=3)
    kb_ctx = "\n".join(f"[{r['title']}]\n{r['excerpt']}" for r in kb_results)

    response = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=512,
        system=SUPPORT_SYSTEM,
        messages=[
            {"role": "user", "content": (
                f"## User History\n{memory_ctx}\n\n"
                f"## Knowledge Base\n{kb_ctx}\n\n"
                f"## User Message\n{message}"
            )}
        ]
    )

    text = response.content[0].text
    escalate = "ESCALATE" in text
    return {"reply": text.replace("ESCALATE", "").strip(), "escalate": escalate}
```

## Failure Modes

| Failure | Cause | Fix |
|---|---|---|
| Hallucinated features | No KB match, model fills gap | Strict grounding: only answer from KB context |
| Escalation storm | Low KB coverage → all < 0.8 | Expand KB; add fallback scripted answers |
| Memory poisoning | Old irrelevant tickets injected | Filter memories by recency + topic similarity |
| Tone mismatch | Sentiment model wrong | Use LLM itself to detect sentiment from message |

## Related

- `skills/03-memory/memory-injection.md`
- `blueprints/rag-stack.md`
- `systems/research-agent.md`

## Changelog

- `v1` (2026-04) — Initial bot with memory injection, intent routing, confidence-gated escalation
