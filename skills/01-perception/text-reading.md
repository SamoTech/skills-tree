# Text Reading

**Category:** `perception`  
**Skill Level:** `basic`  
**Stability:** `stable`

### Description

Parses and understands plain text input in any language or format. The foundational perception skill present in all LLM-based agents.

### Inputs

| Input | Type | Required | Description |
|---|---|---|---|
| `text` | `string` | ✅ | Raw text to parse |
| `language` | `string` | ❌ | Optional language hint |

### Outputs

| Output | Type | Description |
|---|---|---|
| `understanding` | `string` | Internal representation of the text content |

### Example

```python
agent.perceive("The user wants to book a flight to Cairo on Monday.")
# Agent extracts: intent=book_flight, destination=Cairo, date=next_monday
```

### Frameworks

- All LLM frameworks — built-in to every model

### Related Skills

- [Document Parsing](document-parsing.md)
- [Structured Data Reading](structured-data-reading.md)
