"""Skill: auto_skill_generator — use LLM to generate a new skill Python module."""
from __future__ import annotations
import re
from pathlib import Path
from openai import AsyncOpenAI
from agentforge.skills.base import BaseSkill, SkillInput, SkillOutput
from agentforge.core.config import settings
from agentforge.core.logger import logger

SYSTEM_PROMPT = """
You are an expert Python developer specializing in AI agent skills.
Generate a complete AgentForge skill class following this exact template:

```python
from agentforge.skills.base import BaseSkill, SkillInput, SkillOutput

class MySkill(BaseSkill):
    name = "skill_name"          # snake_case, unique
    description = "..."          # one clear sentence
    category = "..."             # e.g. web, code, data, communication
    tags = ["tag1", "tag2"]
    level = "basic"              # basic | intermediate | advanced
    input_schema = {
        "param": {"type": "string", "required": True, "description": "..."}
    }
    output_schema = {
        "result": {"type": "string"}
    }

    async def execute(self, inp: SkillInput) -> SkillOutput:
        # implementation
        ...
        return SkillOutput(success=True, data={"result": "..."})
```

Return ONLY the Python code block. No explanations.
"""


class AutoSkillGeneratorSkill(BaseSkill):
    name = "auto_skill_generator"
    description = "Generate a new AgentForge skill Python module from a natural language description."
    category = "meta"
    tags = ["codegen", "llm", "auto", "scaffold", "plugin"]
    level = "advanced"
    input_schema = {
        "description": {"type": "string", "required": True, "description": "What the skill should do"},
        "model": {"type": "string", "default": "gpt-4o"},
        "save": {"type": "boolean", "default": False, "description": "Save to skills/catalog/"},
    }
    output_schema = {
        "code": {"type": "string"},
        "skill_name": {"type": "string"},
        "file_path": {"type": "string"},
        "category": {"type": "string"},
    }

    async def execute(self, inp: SkillInput) -> SkillOutput:
        description = inp.data.get("description", "")
        model = inp.data.get("model", settings.openai_default_model)
        save = inp.data.get("save", False)

        if not description:
            return SkillOutput(success=False, error="description is required")

        client = AsyncOpenAI(api_key=settings.openai_api_key)
        response = await client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": f"Create a skill that: {description}"},
            ],
            temperature=0.2,
        )
        raw_code = response.choices[0].message.content.strip()

        # Extract code from markdown block if wrapped
        code_match = re.search(r"```python\n(.+?)```", raw_code, re.DOTALL)
        code = code_match.group(1) if code_match else raw_code

        # Extract skill name and category
        name_match = re.search(r'name\s*=\s*["\']([\w_]+)["\']', code)
        cat_match = re.search(r'category\s*=\s*["\']([\w_]+)["\']', code)
        skill_name = name_match.group(1) if name_match else "generated_skill"
        category = cat_match.group(1) if cat_match else "general"

        file_path = None
        if save:
            catalog_dir = Path(__file__).parent
            file_path = str(catalog_dir / f"{skill_name}.py")
            Path(file_path).write_text(code)
            logger.info("auto_skill_generator.saved", path=file_path)

        return SkillOutput(
            success=True,
            data={
                "code": code,
                "skill_name": skill_name,
                "file_path": file_path or f"skills/catalog/{skill_name}.py",
                "category": category,
            },
            metadata={"tokens": response.usage.total_tokens},
        )
