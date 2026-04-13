---
id: lab-tooluse-dynamic-gen
title: Dynamic Tool Generation
category: tool-use
status: experimental
stability: alpha
author: OssamaHashim
updated: 2026-04-13
tags: [tool-use, dynamic, code-generation, labs, experimental]
readiness: Alpha — proof-of-concept only; significant safety review required before production
---

# Lab: Dynamic Tool Generation

> **⚗️ Experimental (Alpha)** — High-risk, high-reward. An agent writes its own tools at runtime. Requires sandboxed execution. Do not deploy without rigorous security review.

## What Is It?

Instead of a fixed tool registry, the agent **generates Python functions on-the-fly** when it encounters a task for which no existing tool is adequate. Generated functions are validated, sandboxed, and added to the tool registry for the remainder of the session.

## Why It's Interesting

- Enables truly open-ended agents that self-extend
- Reduces need for exhaustive upfront tool design
- Agent can specialise tools to the exact task at hand

## ⚠️ Security Warning

Dynamic code execution is inherently dangerous. This prototype:
- Runs generated code in a **restricted `exec()` environment** (no `import os`, no `__builtins__`)
- Is **not suitable for production** without a proper sandbox (gVisor, Firecracker, etc.)
- Should never be given network or filesystem access in any non-sandboxed environment

## Prototype

```python
import anthropic, re, ast
from typing import Callable

client = anthropic.Anthropic()

# Restricted builtins — no I/O, no imports, no exec/eval
SAFE_BUILTINS = {
    'abs': abs, 'round': round, 'len': len, 'range': range,
    'sum': sum, 'min': min, 'max': max, 'sorted': sorted,
    'enumerate': enumerate, 'zip': zip, 'map': map, 'filter': filter,
    'list': list, 'dict': dict, 'set': set, 'tuple': tuple,
    'str': str, 'int': int, 'float': float, 'bool': bool,
    'isinstance': isinstance, 'type': type, 'print': print,
}

def generate_tool(task_description: str) -> tuple[str, Callable]:
    """Ask the model to generate a Python function for the given task."""
    prompt = f"""Write a single Python function to perform this task:
{task_description}

Rules:
- Only use built-in Python functions (no imports)
- Function must have a clear name and type hints
- Include a single-line docstring
- Return the result, do not print
- Wrap the function in ```python ... ``` fences"""

    resp = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=512,
        messages=[{"role": "user", "content": prompt}]
    )
    raw = resp.content[0].text
    match = re.search(r'```python\n(.+?)\n```', raw, re.DOTALL)
    if not match:
        raise ValueError("Model did not return a valid code block")
    code = match.group(1).strip()

    # Safety: parse AST and reject any imports or dangerous nodes
    tree = ast.parse(code)
    for node in ast.walk(tree):
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            raise SecurityError(f"Generated code contains import statement: {ast.dump(node)}")
        if isinstance(node, ast.Call):
            if isinstance(node.func, ast.Name) and node.func.id in ('exec', 'eval', 'compile', '__import__'):
                raise SecurityError(f"Generated code calls forbidden function: {node.func.id}")

    # Compile and exec in restricted environment
    namespace = {'__builtins__': SAFE_BUILTINS}
    exec(compile(tree, '<generated>', 'exec'), namespace)

    # Extract the first function defined
    fn_name = next(
        node.name for node in ast.walk(tree)
        if isinstance(node, ast.FunctionDef)
    )
    return fn_name, namespace[fn_name]

# Usage
class SecurityError(Exception):
    pass

fn_name, fn = generate_tool(
    "Given a list of strings, return a new list with duplicates removed, preserving order"
)
print(f"Generated function: {fn_name}")
result = fn(['a', 'b', 'a', 'c', 'b'])
print(result)  # Expected: ['a', 'b', 'c']
```

## Graduation Criteria

- [ ] Integration with a proper sandbox (gVisor or subprocess with seccomp)
- [ ] Tool caching and reuse across sessions benchmarked
- [ ] Security audit completed
- [ ] Test suite: 50 task descriptions → generated tools pass unit tests
- [ ] Failure rate (model generates invalid/unsafe code) measured and mitigated
