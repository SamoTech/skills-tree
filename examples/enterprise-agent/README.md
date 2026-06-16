# Example: Enterprise Agent Orchestrator

A production-grade multi-agent orchestration system using Skills Tree for skill-based routing, agent manifest validation, and compliance auditing.

## What it demonstrates

- Skill-based task routing (match task → agent by declared skill IDs)
- Agent manifest validation against the Skills Tree taxonomy
- Audit logging of skill invocations per task
- Detection of unknown or deprecated skills in agent manifests
- Pluggable agent registry from JSON

## Setup

```bash
pip install -r requirements.txt
```

## Run

```bash
# Route and execute a task
python orchestrator.py --task "search and summarize AI safety papers"

# Audit all agent manifests
python orchestrator.py --audit

# List available agents and their skills
python orchestrator.py --list-agents
```

## Agent Manifest Format

Each agent declares its skills using canonical Skills Tree IDs:

```json
{
  "name": "researcher",
  "skills": ["web-search", "rag", "summarization"],
  "description": "Researches topics and produces summaries"
}
```
