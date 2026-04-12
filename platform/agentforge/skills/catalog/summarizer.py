"""Skill: summarizer — summarize long text using an LLM."""
from __future__ import annotations
from openai import AsyncOpenAI
from agentforge.skills.base import BaseSkill, SkillInput, SkillOutput
from agentforge.core.config import settings


class SummarizerSkill(BaseSkill):
    name = "summarizer"
    description = "Summarize long text into a concise paragraph or bullet list using an LLM."
    category = "communication"
    tags = ["summarize", "nlp", "text", "condense", "tldr"]
    level = "basic"
    input_schema = {
        "text": {"type": "string", "required": True, "description": "Text to summarize"},
        "style": {"type": "string", "default": "paragraph", "enum": ["paragraph", "bullets", "one_line"]},
        "max_words": {"type": "integer", "default": 150},
        "model": {"type": "string", "default": "gpt-4o-mini"},
    }
    output_schema = {
        "summary": {"type": "string"},
        "word_count": {"type": "integer"},
    }

    async def execute(self, inp: SkillInput) -> SkillOutput:
        text = inp.data.get("text", "")
        style = inp.data.get("style", "paragraph")
        max_words = int(inp.data.get("max_words", 150))
        model = inp.data.get("model", settings.openai_default_model)

        if not text.strip():
            return SkillOutput(success=False, error="No text provided")

        style_instruction = {
            "paragraph": f"Write a concise paragraph summary in under {max_words} words.",
            "bullets": f"Write a bullet-point summary with at most 7 key points.",
            "one_line": "Write a single sentence summary (max 25 words).",
        }.get(style, "Summarize concisely.")

        client = AsyncOpenAI(api_key=settings.openai_api_key)
        response = await client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": f"You are an expert summarizer. {style_instruction}"},
                {"role": "user", "content": text[:12000]},
            ],
            temperature=0.3,
        )
        summary = response.choices[0].message.content.strip()
        return SkillOutput(
            success=True,
            data={"summary": summary, "word_count": len(summary.split())},
            metadata={"tokens": response.usage.total_tokens},
        )
