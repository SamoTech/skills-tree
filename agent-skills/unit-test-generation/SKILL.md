---
name: unit-test-generation
description: Generate focused unit tests that verify isolated behavior, edge cases, and failure handling from explicit contracts.
license: MIT
metadata:
  source: skills/05-code/unit-test-generation.md
  version: "v2"
---

# Unit Test Generation

1. Read the behavior contract and existing test conventions.
2. Identify normal, boundary, and failure cases.
3. Create deterministic tests with meaningful assertions.
4. Mock only dependencies that are outside the unit boundary.
5. Run the focused tests and the relevant broader suite.
6. Record verification evidence.

## Failure modes
- Testing implementation details.
- Missing boundary cases.
- Excessive mocking.
- Weak assertions or flaky setup.

## Evidence
Canonical skill: skills/05-code/unit-test-generation.md
Repository governance: AI_CONSTITUTION.md
