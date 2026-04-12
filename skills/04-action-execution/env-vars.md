# Environment Variable Management

**Category:** `action-execution`  
**Skill Level:** `basic`  
**Stability:** `stable`
**Added:** 2025-03

### Description

Read, set, and manage environment variables for configuration and secret injection in agent workflows.

### Example

```python
import os
from dotenv import load_dotenv

load_dotenv()  # Load .env file
api_key = os.environ.get('OPENAI_API_KEY')
os.environ['LOG_LEVEL'] = 'DEBUG'
```

### Related Skills

- [Shell Command](shell-command.md)
- [Secret Scanning](../14-security/secret-scanning.md)
