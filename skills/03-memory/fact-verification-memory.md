# Fact Verification Memory

**Category:** `memory`  
**Skill Level:** `advanced`  
**Stability:** `stable`

### Description

Maintain a cache of previously verified or refuted facts to avoid re-checking them and to ground future reasoning.

### Example

```python
verified = {}

def store_fact(claim, is_true, source=None):
    verified[claim] = {'verified': is_true, 'source': source}

def is_known(claim):
    return claim in verified
```

### Related Skills

- [Semantic Memory](semantic-memory.md)
- [Self-Correction](../02-reasoning/self-correction.md)
