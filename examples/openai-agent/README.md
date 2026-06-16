# Example: OpenAI Skill-Aware Agent

An OpenAI-powered agent that uses Skills Tree to dynamically select and apply the right skills for each user request.

## What it demonstrates

- Searching Skills Tree by intent
- Enriching OpenAI system prompts with skill context
- Logging which skills were invoked
- Graceful fallback when no matching skill is found

## Setup

```bash
pip install -r requirements.txt
export OPENAI_API_KEY=sk-...
```

## Run

```bash
python agent.py "how do I build a memory system for my agent?"
python agent.py "what is chain-of-thought reasoning?"
python agent.py "show me how to implement tool use"
```

## How it works

1. User sends a query
2. `agent.py` searches Skills Tree for relevant skills
3. Skill descriptions and code examples are injected into the system prompt
4. OpenAI generates a response grounded in the skill taxonomy
5. Response includes which skill IDs were used as context
