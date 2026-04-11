# Handwriting Recognition

**Category:** `perception`  
**Skill Level:** `advanced`  
**Stability:** `experimental`

### Description

Convert handwritten text in images or scanned documents into machine-readable digital text.

### Example

```python
response = client.chat.completions.create(
    model='gpt-4o',
    messages=[{'role': 'user', 'content': [
        {'type': 'text', 'text': 'Transcribe the handwritten text in this image exactly.'},
        {'type': 'image_url', 'image_url': {'url': handwriting_url}}
    ]}]
)
```

### Related Skills

- [OCR](ocr.md)
- [Document Parsing](document-parsing.md)
