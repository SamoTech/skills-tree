# Chart Reading

**Category:** `perception`  
**Skill Level:** `intermediate`  
**Stability:** `stable`

### Description

Interpret charts, graphs, and data visualizations from images to extract numerical values, trends, and patterns.

### Example

```python
response = client.chat.completions.create(
    model='gpt-4o',
    messages=[{'role': 'user', 'content': [
        {'type': 'text', 'text': 'Read the values from this bar chart and list them as JSON.'},
        {'type': 'image_url', 'image_url': {'url': chart_url}}
    ]}]
)
```

### Related Skills

- [Image Understanding](image-understanding.md)
- [OCR](ocr.md)
