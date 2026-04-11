# Dockerfile Generation

**Category:** `code`  
**Skill Level:** `intermediate`  
**Stability:** `stable`

### Description

Generate optimized Dockerfiles for containerizing applications, including multi-stage builds, layer caching, and security best practices.

### Example

```dockerfile
# Generated multi-stage Python Dockerfile
FROM python:3.12-slim AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

FROM python:3.12-slim
WORKDIR /app
COPY --from=builder /usr/local/lib/python3.12 /usr/local/lib/python3.12
COPY . .
CMD ["python", "main.py"]
```

### Related Skills

- [CI/CD Generation](cicd-generation.md)
- [Dependency Management](dependency-management.md)
