# Constraint Satisfaction

**Category:** `reasoning`  
**Skill Level:** `advanced`  
**Stability:** `stable`
**Added:** 2025-03

### Description

Find solutions that satisfy a set of hard and soft constraints simultaneously — scheduling, configuration, assignment problems.

### Example

```python
from constraint import Problem
prob = Problem()
prob.addVariables(['A','B','C'], range(1, 5))
prob.addConstraint(lambda a,b: a != b, ('A','B'))
prob.addConstraint(lambda b,c: b < c, ('B','C'))
solutions = prob.getSolutions()
```

### Related Skills

- [Planning](planning.md)
- [Decision Making](decision-making.md)
