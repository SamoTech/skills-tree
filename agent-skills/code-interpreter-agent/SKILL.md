---
name: code-interpreter-agent
description: Repository-backed code skill for code interpreter agent.
license: MIT
metadata:
  source: skills/05-code/code-interpreter-agent.md
  version: "v2"
---

# code-interpreter-agent

1. Load explicit requirements and repository context.
2. Apply the skill procedure without bypassing validation or security controls.
3. Verify outputs against observable acceptance criteria.
4. Report evidence and unresolved limitations.

## Failure modes

- Inventing requirements or behavior.
- Making unrelated changes.
- Skipping verification.
- Claiming success without evidence.

## Evidence

- skills/05-code/code-interpreter-agent.md
- AI_CONSTITUTION.md
- AGENTS.md

Evidence status: repository-backed implementation guidance; no benchmark claim.
