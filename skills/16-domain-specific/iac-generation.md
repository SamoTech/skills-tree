---
title: "Iac Generation"
category: 16-domain-specific
level: advanced
stability: stable
description: "Apply iac generation in AI agent workflows."
added: "2025-03"
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-16-domain-specific-iac-generation.json)

**Category:** Domain-Specific
**Skill Level:** `advanced`
**Stability:** stable
**Added:** 2026-04

### Description
Generates production-ready Infrastructure as Code (IaC) for Terraform, Ansible, Pulumi, or Kubernetes YAML from natural-language specifications. Applies best practices such as variable parameterisation, state backend configuration, and least-privilege IAM policies.

### Example
```python
import anthropic

client = anthropic.Anthropic()

def generate_terraform(spec: str) -> str:
    prompt = (
        "Generate a production-ready Terraform module for the following spec.\n"
        "Apply best practices: remote state, variables file, outputs, and least-privilege IAM.\n\n"
        + spec
    )
    resp = client.messages.create(
        model="claude-opus-4-5", max_tokens=1500,
        messages=[{"role": "user", "content": prompt}]
    )
    return resp.content[0].text

print(generate_terraform("AWS S3 bucket for static website with CloudFront CDN and OAC"))
```

### Related Skills
- [Code Generation](../05-code/code-generation.md)
- [CI/CD Generation](../05-code/cicd-generation.md)
- [Incident Response](incident-response.md)
