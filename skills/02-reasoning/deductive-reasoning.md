# Deductive Reasoning

**Category:** `reasoning`  
**Skill Level:** `basic`  
**Stability:** `stable`  
**Added:** 2025-03  
**Version:** v2

---

## Description

Derive necessary conclusions from given premises using formal logic. If the premises are true and the argument is valid, the conclusion **must** be true. Deductive reasoning is the foundation of formal proofs, rule-based systems, constraint checking, and any task requiring guaranteed correct inference.

---

## Core Forms

### Modus Ponens
```
Premise 1: If P then Q  (P → Q)
Premise 2: P is true
Conclusion: Therefore Q is true

Example:
  P1: If a user has admin role, they can delete records.
  P2: Alice has admin role.
  C:  Alice can delete records. ✓
```

### Modus Tollens
```
Premise 1: If P then Q  (P → Q)
Premise 2: Q is false
Conclusion: Therefore P is false

Example:
  P1: If the build passes, tests are green.
  P2: Tests are NOT green.
  C:  The build did NOT pass. ✓
```

### Hypothetical Syllogism
```
P1: If A then B
P2: If B then C
C:  If A then C

Example:
  P1: If temperature > 90°C, alarm triggers.
  P2: If alarm triggers, system shuts down.
  C:  If temperature > 90°C, system shuts down.
```

---

## Prompt Pattern

```
Given these rules (premises):
1. [RULE 1]
2. [RULE 2]
...

And these facts:
- [FACT 1]
- [FACT 2]

What can we conclude? Show each deductive step explicitly.
Label each step: Premise / Given / Modus Ponens / Modus Tollens / Contradiction.
```

---

## Common Fallacies to Avoid

| Fallacy | Structure | Why It Fails |
|---|---|---|
| Affirming the consequent | Q is true → P must be true | Multiple causes can produce Q |
| Denying the antecedent | P is false → Q must be false | Q may have other causes |
| Undistributed middle | All A are B; All C are B → A=C | B is shared but A,C may differ |

---

## Related Skills

- [Inductive Reasoning](inductive-reasoning.md)
- [Abductive Reasoning](abductive.md)
- [Mathematical Reasoning](mathematical-reasoning.md)
- [Constraint Satisfaction](constraint-satisfaction.md)
