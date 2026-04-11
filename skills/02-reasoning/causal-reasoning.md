# Causal Reasoning

**Category:** `reasoning`  
**Skill Level:** `advanced`  
**Stability:** `stable`

### Description

Identify cause-and-effect relationships between events or variables, distinguishing correlation from causation.

### Example

```
Q: Why did the deployment fail?
A: The config change removed the DB_URL env var → service lost DB connection
   → health check failed → rollback triggered.
```

### Related Skills

- [Counterfactual Reasoning](counterfactual-reasoning.md)
- [Risk Assessment](risk-assessment.md)
