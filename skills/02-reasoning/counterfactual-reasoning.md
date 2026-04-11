# Counterfactual Reasoning

**Category:** `reasoning`  
**Skill Level:** `advanced`  
**Stability:** `stable`

### Description

Reason about hypothetical alternatives — what *would* have happened if a different action had been taken.

### Example

```
Q: If we had cached the API response, would the timeout have occurred?
A: No — the cache would have served the result in <1ms,
   avoiding the upstream latency that caused the timeout.
```

### Related Skills

- [Causal Reasoning](causal-reasoning.md)
- [Risk Assessment](risk-assessment.md)
