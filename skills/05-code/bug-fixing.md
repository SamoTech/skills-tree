---
Category: Code
Skill Level: Advanced
Stability: Stable
Tags: [debugging, bug-fixing, root-cause-analysis, static-analysis, test-repair]
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-05-code-bug-fixing.json)

# Bug Fixing

### Description
Locates and repairs defects in code through static analysis, dynamic execution, log analysis, test failure diagnosis, and root cause identification. Handles runtime errors, logic bugs, race conditions, memory leaks, and security vulnerabilities. Uses execution traces, stack traces, and failing test cases as primary evidence.

### When to Use
- Repairing failing tests or CI/CD pipeline failures automatically
- Analyzing stack traces and logs to identify the root cause of production errors
- Security hardening: fixing detected CVEs or injection vulnerabilities
- Resolving flaky tests by identifying non-deterministic behavior

### Example
```python
from openai import OpenAI
import subprocess, ast

client = OpenAI()

def fix_bug(source_code: str, error_output: str, test_file: str = None) -> str:
    context = f"Source code:\n```python\n{source_code}\n```\nError:\n{error_output}"
    if test_file:
        with open(test_file) as f:
            context += f"\nFailing tests:\n```python\n{f.read()}\n```"

    r = client.chat.completions.create(
        model="o3",
        messages=[{
            "role": "system",
            "content": "You are an expert debugger. Analyze the error and tests, identify the root cause, and return ONLY the corrected source code."
        }, {"role": "user", "content": context}]
    )
    fixed = r.choices[0].message.content.strip()
    # Syntax check before returning
    ast.parse(fixed)
    return fixed

def fix_until_passing(source: str, test_cmd: list[str], max_rounds: int = 5) -> str:
    for _ in range(max_rounds):
        result = subprocess.run(test_cmd, capture_output=True, text=True)
        if result.returncode == 0:
            return source
        source = fix_bug(source, result.stdout + result.stderr)
        with open(test_cmd[-1].replace("test_", ""), "w") as f:
            f.write(source)
    return source
```

### Advanced Techniques
- **Fault localization**: use `pytest-cov` line coverage + spectrum-based fault localization (Tarantula) to rank likely buggy lines
- **Bisect debugging**: `git bisect` automation to find the commit that introduced the regression
- **Dynamic analysis**: instrument code with `sys.settrace` to capture variable states at each line during failing test
- **Fuzzing**: use `hypothesis` to generate edge cases that expose the bug before attempting a fix

### Related Skills
- `code-review`, `code-testing`, `security-audit`, `code-execution`, `self-correction`
