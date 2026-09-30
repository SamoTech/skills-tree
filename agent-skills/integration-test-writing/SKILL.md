---
name: integration-test-writing
description: Create integration tests that verify interactions between real application components, external boundaries, persistence, or services.
license: MIT
metadata:
  source: skills/05-code/integration-test-writing.md
  version: "v2"
---

# Integration Test Writing

1. Identify the real integration boundary and expected observable behavior.
2. Inspect existing fixtures, environment setup, and test conventions.
3. Build deterministic setup and teardown around the boundary.
4. Assert meaningful behavior rather than implementation details.
5. Run the integration suite and inspect failures for environmental versus product causes.
6. Record verification evidence.

## Failure modes
- Mocking away the integration being tested.
- Shared state and flaky setup.
- Weak assertions.
- Uncontrolled external prerequisites.

## Evidence
Canonical skill: skills/05-code/integration-test-writing.md
Repository governance: AI_CONSTITUTION.md
