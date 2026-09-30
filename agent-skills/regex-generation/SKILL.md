---
name: regex-generation
description: Generate regular expressions from explicit matching and rejection requirements and validate them against representative cases.
license: MIT
metadata:
  source: skills/05-code/regex-generation.md
  version: "v2"
---

# Regex Generation

1. Collect required matches and explicit rejection cases.
2. Identify the target regex engine and syntax constraints.
3. Generate the simplest readable pattern that satisfies the cases.
4. Test positive, negative, boundary, and malformed inputs.
5. Check performance for untrusted or large inputs.
6. Record the pattern assumptions and evidence.

## Failure modes
- Overmatching or undermatching.
- Engine incompatibility.
- Missing negative or boundary cases.
- Pathological pattern behavior.

## Evidence
Canonical skill: skills/05-code/regex-generation.md
Repository governance: AI_CONSTITUTION.md
