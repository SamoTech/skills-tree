# Example: Recommendation Engine

A learning path recommender that uses Skills Tree's prerequisite dependency graph to generate personalized skill paths.

## What it demonstrates

- Prerequisite-aware path planning
- Gap analysis between current and target skills
- Difficulty-ordered learning sequences
- CLI interface for integration into tools

## Setup

```bash
pip install -r requirements.txt
```

## Run

```bash
# Get a path from beginner to RAG
python recommend.py --current "python-basics" --target "rag"

# Multiple current skills
python recommend.py --current "python-basics,api-calls,embeddings" --target "production-rag"

# Output as JSON
python recommend.py --current "python-basics" --target "rag" --json
```

## Integration

```python
from recommend import get_learning_path

path = get_learning_path(
    current=["python-basics"],
    target="production-rag"
)
for step in path:
    print(f"{step['order']}. {step['title']} ({step['estimated_hours']}h)")
```
