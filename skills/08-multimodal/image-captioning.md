# Image Captioning

**Category:** `multimodal`  
**Skill Level:** `basic`  
**Stability:** `stable`
**Added:** 2025-03

### Description

Generate a natural language description of the contents of an image.

### Example

```python
response = client.chat.completions.create(
    model='gpt-4o',
    messages=[{'role': 'user', 'content': [
        {'type': 'text', 'text': 'Describe this image in detail.'},
        {'type': 'image_url', 'image_url': {'url': image_url}}
    ]}]
)
caption = response.choices[0].message.content
```

### Related Skills

- [Image Understanding](../01-perception/image-understanding.md)
- [Visual Question Answering](vqa.md)
