# Customer Support Bot System

**Category:** systems | **Level:** intermediate | **Stability:** stable | **Version:** v1

## Overview

A personalized customer support agent that retrieves past interaction history, identifies user intent, generates context-aware responses, escalates when needed, and continuously improves from resolved tickets — combining memory, intent detection, and response generation skills into a production-grade support loop.

---

## Skills Used

| Skill | Role in System |
|---|---|
| `skills/03-memory/memory-injection.md` | Surface past interactions and user profile |
| `skills/03-memory/episodic.md` | Recall specific past support cases |
| `skills/06-communication/intent-detection.md` | Classify the user's underlying need |
| `skills/06-communication/response-generation.md` | Draft the final customer reply |
| `skills/06-communication/tone-adaptation.md` | Match response tone to user sentiment |
| `skills/02-reasoning/decision-making.md` | Decide: resolve, escalate, or ask for more info |
| `skills/15-orchestration/escalation.md` | Route to human agent when confidence is low |

---

## Architecture

```
┌───────────────────────────────────────────────────┐
│               Customer Support Bot                │
├───────────────────────────────────────────────────┤
│                                                   │
│  User Message                                     │
│       │                                           │
│       ▼                                           │
│  Memory Retrieval (top-3 past cases)              │
│       │                                           │
│       ▼                                           │
│  Intent Classifier                                │
│  (billing / technical / general / complaint)      │
│       │                                           │
│       ▼                                           │
│  ┌────────────────────────────┐                   │
│  │     Resolution Router      │                   │
│  │  confidence >= 0.8 → Bot   │                   │
│  │  confidence <  0.8 → Human │                   │
│  └────────┬──────────┬────────┘                   │
│           │          │                            │
│          Bot        Human                         │
│           │        Escalation                     │
│           ▼                                       │
│  Response Generator + Tone Adapter                │
│           │                                       │
│           ▼                                       │
│        Reply + Log to Memory                      │
└───────────────────────────────────────────────────┘
```

---

## Implementation

```python
import anthropic
import json
from dataclasses import dataclass
from typing import Optional

client = anthropic.Anthropic()

@dataclass
class UserProfile:
    user_id: str
    name: str
    plan: str
    past_cases: list[dict]  # [{issue, resolution, date}]
    sentiment_history: list[str]  # ["positive", "frustrated", ...]

SUPPORT_SYSTEM = """
You are a friendly, expert customer support agent.
You have access to the user's profile and past interactions.

Respond with a JSON object:
{
  "intent": "billing|technical|general|complaint|other",
  "confidence": 0.0-1.0,
  "reply": "Your response to the customer",
  "escalate": true/false,
  "escalation_reason": "reason if escalate is true",
  "resolution_status": "resolved|pending|escalated"
}

Tone rules:
- frustrated user → empathetic, apologetic opener
- happy user → warm, efficient
- repeat issue → acknowledge the frustration explicitly
"""

def build_context(profile: UserProfile, message: str) -> str:
    past = json.dumps(profile.past_cases[-3:], indent=2)  # last 3 cases
    sentiment = profile.sentiment_history[-1] if profile.sentiment_history else "neutral"
    return f"""User: {profile.name} | Plan: {profile.plan}
Recent sentiment: {sentiment}
Past cases (last 3):\n{past}\n\nCurrent message: {message}"""

def handle_message(profile: UserProfile, message: str) -> dict:
    context = build_context(profile, message)
    response = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=1024,
        system=SUPPORT_SYSTEM,
        messages=[{"role": "user", "content": context}]
    )
    result = json.loads(response.content[0].text)

    # Log this interaction to memory
    profile.past_cases.append({
        "issue": message,
        "intent": result["intent"],
        "resolution": result["resolution_status"],
        "date": "2026-04-13"
    })
    return result

# Usage
if __name__ == "__main__":
    profile = UserProfile(
        user_id="usr_123",
        name="Ossama",
        plan="Pro",
        past_cases=[
            {"issue": "Billing overcharge", "resolution": "resolved", "date": "2026-03-01"}
        ],
        sentiment_history=["frustrated"]
    )

    result = handle_message(profile, "My API key stopped working after I upgraded.")
    print(result["reply"])
    if result["escalate"]:
        print(f"[ESCALATE] → Human agent: {result['escalation_reason']}")
```

---

## Failure Modes

| Failure | Cause | Mitigation |
|---|---|---|
| Wrong intent | Ambiguous message | Ask one clarifying question before routing |
| Over-escalation | Low confidence threshold | Tune threshold per intent category |
| Memory overload | Too many past cases | Keep only last 10 cases in context |
| Hallucinated policy | LLM invents refund rules | Ground responses in a knowledge base RAG |

---

## Related

- `blueprints/rag-stack.md` — Add product knowledge base for grounded answers
- `skills/03-memory/memory-injection.md` · `skills/06-communication/tone-adaptation.md`
- `systems/research-agent.md` — Escalation path can trigger a research sub-agent

## Changelog

- **v1** (2026-04) — Initial system: memory injection, intent routing, escalation, tone adaptation
