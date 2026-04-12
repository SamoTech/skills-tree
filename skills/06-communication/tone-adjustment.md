# Tone Adjustment

**Category:** `communication`  
**Skill Level:** `basic`  
**Stability:** `stable`
**Added:** 2025-03

### Description

Rewrite or generate text in a specified tone — formal, casual, empathetic, assertive, technical, or humorous — to match the audience and context.

### Example

```python
prompt = f'''
Rewrite the following message in a warm, friendly tone:
"{original_message}"
'''
adjusted = llm.invoke(prompt)
```

### Related Skills

- [Paraphrasing](paraphrasing.md)
- [Persona Adoption](persona-adoption.md)
- [Email Drafting](email-drafting.md)
