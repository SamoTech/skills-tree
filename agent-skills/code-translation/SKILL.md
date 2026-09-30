---
name: code-translation
description: Translate source code between programming languages while preserving behavior, interfaces, and documented constraints.
license: MIT
metadata:
  source: skills/05-code/code-translation.md
  version: "v2"
---

# Code Translation

1. Load the repository state and identify the exact requirement, affected components, and existing contracts.
2. Inspect relevant source, configuration, tests, and documentation before editing.
3. Define the smallest change that satisfies the requirement without weakening quality or security controls.
4. Implement the change with explicit handling for invalid, missing, or incompatible inputs.
5. Run the most relevant repository validation and inspect failures rather than bypassing them.
6. Record concise evidence of the implementation and verification performed.

## Failure modes
- Ambiguous requirements or missing repository context.
- Unintended interface or behavior changes.
- Incomplete tests or verification.
- Validator bypasses or weakened security controls.
- Completion claims without evidence.

## Evidence
- Canonical skill: [skills/05-code/code-translation.md](../../skills/05-code/code-translation.md)
- Repository governance: [AI_CONSTITUTION.md](../../AI_CONSTITUTION.md)
- Agent operating model: [meta/AGENT_OPERATING_MODEL.md](../../meta/AGENT_OPERATING_MODEL.md)
