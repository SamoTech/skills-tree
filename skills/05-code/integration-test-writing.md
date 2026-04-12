# Integration Test Writing

**Category:** `code`  
**Skill Level:** `advanced`  
**Stability:** `stable`
**Added:** 2025-03

### Description

Write tests that verify interactions between multiple components, services, or modules working together.

### Example

```python
import pytest
import httpx

@pytest.mark.integration
def test_create_and_retrieve_skill():
    client = httpx.Client(base_url='http://localhost:8000')
    r = client.post('/skills', json={'slug': 'test-skill', 'category': 'code'})
    assert r.status_code == 201
    skill_id = r.json()['id']
    r2 = client.get(f'/skills/{skill_id}')
    assert r2.json()['slug'] == 'test-skill'
```

### Related Skills

- [Unit Test Generation](unit-test-generation.md)
- [Code Generation](code-generation.md)
