---
title: "Code Generation"
category: 05-code
level: intermediate
stability: stable
description: "Apply code generation in AI agent workflows."
---


![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-05-code-code-generation.json)

# Code Generation

### Description
Generates correct, idiomatic, production-quality code from natural language specifications, existing code context, or test cases. Covers single functions, full modules, multi-file projects, and API integrations. Includes test-driven generation (TDD-style), self-repair loops, and static analysis validation.

### When to Use
- Scaffolding new features, modules, or microservices from specifications
- Test-driven code generation: generate implementation from failing tests
- Translating pseudocode, diagrams, or requirements into executable code
- Auto-generating boilerplate (CRUD endpoints, data models, migrations)

### Example
```python
from openai import OpenAI
import subprocess, textwrap

client = OpenAI()

def generate_and_validate(spec: str, language: str = "python") -> str:
    """Generate code, run linter, self-repair if linting fails."""
    prompt = f"""Generate {language} code for the following specification.
Output ONLY the code, no explanation, no markdown fences.
Specification: {spec}"""

    for attempt in range(3):
        r = client.chat.completions.create(
            model="o3",
            messages=[{"role": "user", "content": prompt}]
        )
        code = r.choices[0].message.content.strip()

        # Write to temp file and lint
        with open("/tmp/gen_code.py", "w") as f:
            f.write(code)
        result = subprocess.run(["ruff", "check", "/tmp/gen_code.py"], capture_output=True, text=True)
        if result.returncode == 0:
            return code

        # Feed lint errors back for self-repair
        prompt = f"""The following code has lint errors. Fix them.
Code:\n```python\n{code}\n```\nErrors: {result.stdout}
Output ONLY the fixed code."""

    return code  # return best attempt
```

### Advanced Techniques
- **TDD generation**: first generate failing tests, then generate implementation until tests pass
- **Multi-file projects**: use a project manifest (list of files + their purposes) and generate each file with cross-file context
- **Compiler-in-the-loop**: for compiled languages (Go, Rust, TypeScript), compile and feed errors back
- **RAG-enhanced**: retrieve similar code from the codebase before generating to ensure style consistency

### Related Skills
- `code-review`, `bug-fixing`, `code-testing`, `refactoring`, `code-execution`
