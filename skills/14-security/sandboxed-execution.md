![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-14-security-sandboxed-execution.json)

**Category:** Security
**Skill Level:** `advanced`
**Stability:** stable
**Added:** 2026-04

### Description
Runs agent-generated or user-supplied code in an isolated execution environment with restricted filesystem access, network egress controls, and resource limits. Captures stdout/stderr and enforces timeouts.

### Example
```python
import subprocess, resource, tempfile, os

def run_sandboxed(code: str, timeout: int = 5) -> dict:
    with tempfile.NamedTemporaryFile(suffix=".py", mode="w", delete=False) as f:
        f.write(code)
        script = f.name
    try:
        result = subprocess.run(
            ["python3", script],
            capture_output=True, text=True, timeout=timeout,
            # Restrict to read-only rootfs in real deployment (seccomp / nsjail)
        )
        return {"stdout": result.stdout, "stderr": result.stderr,
                "returncode": result.returncode}
    except subprocess.TimeoutExpired:
        return {"error": "timeout", "returncode": -1}
    finally:
        os.unlink(script)

print(run_sandboxed("print(2 ** 32)"))
```

### Related Skills
- [Input Sanitization](input-sanitization.md)
- [Code Execution Sandbox](../05-code/code-execution-sandbox.md)
