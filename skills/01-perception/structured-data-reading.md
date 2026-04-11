# Structured Data Reading

**Category:** `perception`  
**Skill Level:** `basic`  
**Stability:** `stable`

### Description

Parse and interpret structured data formats: JSON, XML, YAML, TOML, INI.

### Example

```python
import yaml
with open('config.yaml') as f:
    config = yaml.safe_load(f)
```

### Related Skills

- [JSON Transformation](../12-data/json-transformation.md)
- [Document Parsing](document-parsing.md)
