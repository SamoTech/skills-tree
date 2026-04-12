"""Skill: image_analyzer — analyze images using OpenAI Vision."""
from __future__ import annotations
import base64
from pathlib import Path
from openai import AsyncOpenAI
from agentforge.skills.base import BaseSkill, SkillInput, SkillOutput
from agentforge.core.config import settings


class ImageAnalyzerSkill(BaseSkill):
    name = "image_analyzer"
    description = "Analyze an image (URL or local path) using OpenAI Vision and return a description."
    category = "multimodal"
    tags = ["vision", "image", "ocr", "vqa", "gpt-4o", "describe"]
    level = "intermediate"
    input_schema = {
        "image": {"type": "string", "required": True, "description": "Image URL or local file path"},
        "prompt": {"type": "string", "default": "Describe this image in detail."},
        "model": {"type": "string", "default": "gpt-4o"},
    }
    output_schema = {
        "description": {"type": "string"},
        "tokens": {"type": "integer"},
    }

    async def execute(self, inp: SkillInput) -> SkillOutput:
        image = inp.data.get("image", "")
        prompt = inp.data.get("prompt", "Describe this image in detail.")
        model = inp.data.get("model", "gpt-4o")

        if not image:
            return SkillOutput(success=False, error="image is required")

        # Build image content
        if image.startswith("http"):
            image_content = {"type": "image_url", "image_url": {"url": image}}
        else:
            path = Path(image)
            if not path.exists():
                return SkillOutput(success=False, error=f"File not found: {image}")
            b64 = base64.b64encode(path.read_bytes()).decode()
            ext = path.suffix.lstrip(".").lower() or "jpeg"
            image_content = {"type": "image_url", "image_url": {"url": f"data:image/{ext};base64,{b64}"}}

        client = AsyncOpenAI(api_key=settings.openai_api_key)
        response = await client.chat.completions.create(
            model=model,
            messages=[{
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    image_content,
                ],
            }],
            max_tokens=1000,
        )
        description = response.choices[0].message.content.strip()
        return SkillOutput(
            success=True,
            data={"description": description, "tokens": response.usage.total_tokens},
        )
