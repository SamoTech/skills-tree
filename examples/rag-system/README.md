# Example: RAG System with Skill Context

Demonstrates using Skills Tree as a structured knowledge layer above a RAG pipeline, improving retrieval precision and answer quality.

## What it demonstrates

- Using skill search to identify relevant knowledge areas
- Enriching RAG context with structured skill prerequisites
- Building a hybrid retrieval system (semantic + structured)
- Comparing answers with and without skill context

## Setup

```bash
pip install -r requirements.txt
export OPENAI_API_KEY=sk-...  # optional, for LLM responses
```

## Run

```bash
# Basic skill-context retrieval
python rag.py "how do I add memory to my agent?"

# With LLM completion
python rag.py "what is the best approach for tool use?" --llm

# Show context only (no LLM needed)
python rag.py "explain chain of thought" --context-only
```
