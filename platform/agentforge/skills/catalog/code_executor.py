"""Skill: code_executor — safely run Python code in a subprocess sandbox."""
from __future__ import annotations
import asyncio
import textwrap
import tempfile
import os
from agentforge.skills.base import BaseSkill, SkillInput, SkillOutput


class CodeExecutorSkill(BaseSkill):
    name = "code_executor"
    description = "Execute Python code in an isolated subprocess and return stdout/stderr."
    category = "code"
    tags = ["python", "execution", "sandbox", "repl"]
    level = "intermediate"
    input_schema = {
        "code": {"type": "string", "required": True, "description": "Python source code to execute"},
        "timeout": {"type": "integer", "default": 10, "description": "Max seconds before kill"},
    }
    output_schema = {
        "stdout": {"type": "string"},
        "stderr": {"type": "string"},
        "exit_code": {"type": "integer"},
    }

    async def execute(self, inp: SkillInput) -> SkillOutput:
        code = inp.data.get("code", "")
        timeout = int(inp.data.get("timeout", 10))
        if not code.strip():
            return SkillOutput(success=False, error="No code provided")

        # Write to temp file and run in subprocess
        with tempfile.NamedTemporaryFile(suffix=".py", mode="w", delete=False) as f:
            f.write(textwrap.dedent(code))
            tmp_path = f.name

        try:
            proc = await asyncio.create_subprocess_exec(
                "python3", tmp_path,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )
            try:
                stdout, stderr = await asyncio.wait_for(proc.communicate(), timeout=timeout)
            except asyncio.TimeoutError:
                proc.kill()
                return SkillOutput(
                    success=False,
                    error=f"Execution timed out after {timeout}s",
                    data={"stdout": "", "stderr": "TimeoutError", "exit_code": -1},
                )
            return SkillOutput(
                success=proc.returncode == 0,
                data={
                    "stdout": stdout.decode(errors="replace"),
                    "stderr": stderr.decode(errors="replace"),
                    "exit_code": proc.returncode,
                },
            )
        finally:
            os.unlink(tmp_path)
