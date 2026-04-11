"""Skill system tests."""
import pytest
from agentforge.skills.base import SkillInput, SkillOutput
from agentforge.skills.registry.registry import SkillRegistry
from agentforge.skills.catalog.llm_generate import LLMGenerateSkill
from agentforge.skills.catalog.summarizer import SummarizerSkill
from agentforge.skills.catalog.http_request import HttpRequestSkill


@pytest.fixture
def registry():
    reg = SkillRegistry()
    reg.register(LLMGenerateSkill())
    reg.register(SummarizerSkill())
    reg.register(HttpRequestSkill())
    return reg


def test_registry_list(registry):
    skills = registry.list_all()
    assert len(skills) >= 3


def test_registry_get(registry):
    skill = registry.get('llm_generate')
    assert skill is not None
    assert skill.name == 'llm_generate'


def test_registry_search(registry):
    results = registry.search('summar')
    assert any(s.name == 'summarizer' for s in results)


def test_skill_metadata(registry):
    for skill in registry.list_all():
        assert skill.name
        assert skill.description
        assert skill.category
        assert isinstance(skill.tags, list)
        assert isinstance(skill.input_schema, dict)
        assert isinstance(skill.output_schema, dict)


@pytest.mark.asyncio
async def test_http_request_skill():
    skill = HttpRequestSkill()
    result = await skill.execute(SkillInput(data={'url': 'https://httpbin.org/get', 'method': 'GET'}))
    assert result.success
