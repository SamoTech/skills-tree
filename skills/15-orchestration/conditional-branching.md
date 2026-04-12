**Category:** Orchestration
**Skill Level:** Intermediate
**Stability:** stable
**Added:** 2025-03

### Description
Routes workflow execution down different paths based on runtime conditions — LLM classification outputs, numeric thresholds, or structured decision trees. Avoids hard-coded if/else chains by using a rule-engine or router pattern.

### Example
```python
import anthropic
import json

client = anthropic.Anthropic()

def classify_intent(user_message: str) -> str:
    """Route to the correct handler based on intent."""
    response = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=64,
        messages=[{"role": "user", "content": (
            f'Classify this request into ONE of: ["code", "data", "creative", "general"].\n'
            f'Request: "{user_message}"\nOutput ONLY the JSON string.'
        )}]
    )
    return json.loads(response.content[0].text)

handlers = {
    "code":     lambda m: f"Running code agent for: {m}",
    "data":     lambda m: f"Running data agent for: {m}",
    "creative": lambda m: f"Running creative agent for: {m}",
    "general":  lambda m: f"Running general agent for: {m}",
}

message = "Write a Python script to parse CSV files"
intent = classify_intent(message)
result = handlers.get(intent, handlers["general"])(message)
print(f"Intent: {intent} → {result}")
```

### Related Skills
- [Sequential Workflow](sequential-workflow.md)
- [Role Assignment](role-assignment.md)
- [Agent Handoff](agent-handoff.md)
