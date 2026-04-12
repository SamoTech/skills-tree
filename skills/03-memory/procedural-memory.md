# Procedural Memory

**Category:** `memory`  
**Skill Level:** `intermediate`  
**Stability:** `stable`
**Added:** 2025-03

### Description

Store and recall step-by-step procedures, workflows, and skill patterns the agent has learned or been taught.

### Example

```python
procedures = {
    'deploy_app': [
        'Run unit tests',
        'Build Docker image',
        'Push to registry',
        'Apply k8s manifest',
        'Monitor rollout'
    ]
}

def recall(name):
    return procedures.get(name, [])
```

### Related Skills

- [Semantic Memory](semantic-memory.md)
- [Planning](../02-reasoning/planning.md)
