# Structured Output

**Category:** `communication`  
**Skill Level:** `intermediate`  
**Stability:** `stable`
**Added:** 2025-03

### Description

Generate output in a structured format (JSON, YAML, CSV, XML, Markdown table) that can be parsed and used programmatically.

### Example

```python
from pydantic import BaseModel
from openai import OpenAI

class Skill(BaseModel):
    slug: str
    category: str
    level: str

client = OpenAI()
response = client.beta.chat.completions.parse(
    model='gpt-4o',
    messages=[{'role': 'user', 'content': 'Extract the skill info from: tree-of-thought is an advanced reasoning skill.'}],
    response_format=Skill
)
print(response.choices[0].message.parsed)
```

### Related Skills

- [Instruction Following](instruction-following.md)
- [JSON Transformation](../12-data/json-transformation.md)
