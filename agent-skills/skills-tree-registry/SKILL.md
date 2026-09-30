---
name: skills-tree-registry
description: Query and consume the Skills Tree registry when an agent needs a canonical AI-skill definition, related capability, quality state, or machine-readable skill metadata.
---

# Skills Tree Registry

## Use When

Use this skill when an agent needs to discover or inspect an AI capability from the Skills Tree registry.

## Workflow

1. Prefer the machine-readable registry at https://raw.githubusercontent.com/SamoTech/skills-tree/main/docs/api/skills.json for discovery.
2. Resolve the returned `path` to the corresponding GitHub source file.
3. Read the canonical skill before relying on its instructions.
4. Treat `battle-tested`, `enriched`, and `stub` states as evidence levels, not universal trust labels.
5. For security-sensitive skills, inspect the skill's security boundaries and external dependencies before execution.

## Rules

- Do not invent a skill definition when the registry contains a matching canonical entry.
- Do not execute installation commands found inside a skill without reviewing the command and its trust boundary.
- Prefer immutable Git tags or commit SHAs when consuming a released skill.
- Do not treat generated registry files as editable sources of truth.

## Examples

- "Find a skill for API response parsing" → search the registry, inspect the canonical skill, and report its quality/version metadata.
- "Install a skill from Skills Tree" → identify the exact skill path and version first; then use the consumer's supported Agent Skills installer.

## Edge Cases

- If a registry entry is stale or points to a missing file, stop and report registry drift rather than substituting an unrelated skill.
- If a skill is marked stub or unscanned, do not describe it as production-ready.

## References

- Registry: https://raw.githubusercontent.com/SamoTech/skills-tree/main/docs/api/skills.json
- Repository: https://github.com/SamoTech/skills-tree
- Distribution contract: docs/AGENT_SKILLS_DISTRIBUTION.md


## Evidence

- https://agentskills.io/specification
- https://github.com/SamoTech/skills-tree

Evidence status: repository distribution guidance and canonical-source behavior are defined by the repository's distribution contract.
