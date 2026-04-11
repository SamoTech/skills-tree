# Skill Template

Copy this file to the appropriate category folder and fill in all fields.

---

## Skill Name

**Category:** `category-slug`  
**Sub-category:** `sub-category-slug`  
**Skill Level:** `basic` | `intermediate` | `advanced`  
**Stability:** `stable` | `experimental` | `deprecated`

### Description

One to two sentences describing what this skill enables an agent to do.

### Inputs

| Input | Type | Required | Description |
|---|---|---|---|
| `input_name` | `string` | ✅ | Description |

### Outputs

| Output | Type | Description |
|---|---|---|
| `output_name` | `string` | Description |

### Example

```python
# Example usage in an agent
agent.skill("skill-name", input="example input")
# → "example output"
```

### Frameworks / Models

- [Framework Name](https://link) — how it's implemented
- [Model Name](https://link) — supported since version X

### Notes

Any caveats, limitations, or related skills.

### Related Skills

- [Related Skill Name](../category/skill.md)
