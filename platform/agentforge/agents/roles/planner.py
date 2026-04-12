"""Planner Agent — decomposes user goals into executable sub-tasks."""
from __future__ import annotations
import json
from agentforge.agents.base import BaseAgent, AgentInput, AgentOutput
from agentforge.core.logger import logger


class PlannerAgent(BaseAgent):
    role = "planner"
    default_system_prompt = """
You are a Planner Agent. Your job is to decompose a user's goal into
an ordered list of concrete sub-tasks that can be executed by specialist agents.

Respond ONLY with a JSON array of task objects:
[
  {"step": 1, "task": "...", "skill": "skill_name", "depends_on": []},
  ...
]

Available skills: {skill_list}
"""

    async def run(self, inp: AgentInput) -> AgentOutput:
        registry = inp.context.get("skill_registry")
        skill_names = [s.name for s in registry.list_all()] if registry else []

        prompt = self.default_system_prompt.format(
            skill_list=", ".join(skill_names[:50])
        )

        response = await self.llm_call(
            system=prompt,
            user=inp.goal,
            model=self.model,
        )

        try:
            plan = json.loads(response)
        except json.JSONDecodeError:
            logger.warning("planner.parse_failed", raw=response[:200])
            plan = [{"step": 1, "task": inp.goal, "skill": "llm_generate", "depends_on": []}]

        logger.info("planner.plan_created", steps=len(plan))
        return AgentOutput(
            result=json.dumps(plan, indent=2),
            metadata={"plan": plan, "step_count": len(plan)},
        )
