**Category:** Security & Safety
**Skill Level:** Intermediate
**Stability:** stable
**Added:** 2025-03

### Description
Runs untrusted or agent-generated code inside an isolated environment (Docker container, gVisor, Pyodide WASM) that blocks network access, limits CPU/memory, and prevents filesystem escapes. Returns stdout/stderr without exposing the host system.

### Example
```python
import docker
import tempfile, os

client = docker.from_env()

def run_sandboxed(code: str, timeout: int = 10) -> str:
    """Execute Python code in a restricted Docker container."""
    with tempfile.NamedTemporaryFile(suffix=".py", mode="w", delete=False) as f:
        f.write(code)
        script_path = f.name

    try:
        result = client.containers.run(
            image="python:3.12-slim",
            command=["python", "/sandbox/script.py"],
            volumes={os.path.dirname(script_path): {"bind": "/sandbox", "mode": "ro"}},
            network_disabled=True,
            mem_limit="64m",
            cpu_period=100_000,
            cpu_quota=25_000,   # 25% CPU
            remove=True,
            stdout=True,
            stderr=True,
            timeout=timeout,
        )
        return result.decode()
    except docker.errors.ContainerError as e:
        return f"Error: {e.stderr.decode()}"
    finally:
        os.unlink(script_path)

output = run_sandboxed("print(sum(range(100)))")
print(output)  # 4950
```

### Related Skills
- [Code Execution Sandbox](../05-code/code-execution-sandbox.md)
- [Permission Checking](permission-checking.md)
- [Audit Logging](audit-logging.md)
