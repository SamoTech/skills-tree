---
name: tool-invention
description: Close capability gaps by designing, implementing, and validating new tools at runtime when no existing tool fits, with each invented tool reviewed, tested, and registered before reuse.
metadata:
  source: skills/09-agentic-patterns/tool-invention.md
  category: 09-agentic-patterns
  version: "v1"
---

# Tool Invention

Category: Agentic Patterns | Level: advanced | Stability: experimental | Version: v1

## Description

An agent that only uses the tools it was given stalls the first time a task needs a missing primitive. Tool invention closes that gap deliberately: confirm the gap is real, write a minimal contract, implement with tests, validate on held-out cases, and register the tool for reuse. The discipline is what separates invention from improvisation — an invented tool is a durable artifact, not a one-off hack.

## When to Use

Use when a repeated workaround shows a missing primitive: the same task fails or degrades across sessions and no registered tool covers it.

Do not invent tools to bypass an existing restriction; a guardrail that blocks a capability is a boundary, not a gap.

## Inputs

| Input | Type | Required | Description |
|---|---|---|---|
| `task` | `spec` | Yes | The recurring task that exposes the gap |
| `registry` | `list` | Yes | Existing tools with their contracts |
| `evidence` | `list` | Yes | Failing runs or workarounds that show the gap |

## Procedure

1. Confirm the gap: search the tool registry and prove no existing tool fits, citing the failure evidence.
2. Write a minimal contract: purpose, typed inputs and outputs, failure modes, and authority requirements.
3. Implement the smallest tool that satisfies the contract; nothing speculative.
4. Test against representative cases plus held-out cases the contract implies but the task did not show.
5. Review the tool (critic pass or second review) for correctness and boundary violations before first use.
6. Register the tool with a version and changelog; retire it when usage ends.

## Outputs

| Output | Type | Description |
|---|---|---|
| `new_tool` | `artifact` | The implemented tool with tests |
| `validation_report` | `object` | Pass/fail on representative and held-out cases |
| `registry_entry` | `object` | Versioned contract added to the tool registry |

## Runnable Example

```python
def should_invent(evidence, registry, threshold=3):
    distinct_failures = {e["pattern"] for e in evidence if e["kind"] == "missing_tool"}
    covered = {t["name"] for t in registry}
    gaps = [p for p in distinct_failures if p not in covered]
    return {"invent": len(distinct_failures) >= threshold and bool(gaps), "gaps": gaps}

evidence = [
    {"pattern": "pdf_split", "kind": "missing_tool"},
    {"pattern": "pdf_split", "kind": "missing_tool"},
    {"pattern": "pdf_split", "kind": "missing_tool"},
]
print(should_invent(evidence, [{"name": "http_request"}]))
```

## Failure Modes

| Failure Mode | Cause | Mitigation |
|---|---|---|
| Restriction bypass | Tool re-enables a capability a guardrail removed | Review against the boundary; refuse to register |
| Duplicate invention | Registry search skipped | Require the registry check as step one |
| Unvalidated tool | Invented and used in the same breath | Held-out validation before first use |
| Scope creep | The tool grows into a framework | Keep the contract minimal; split later if needed |
| No tests | Only the happy path was exercised | Tests ship with the tool, not after |

## Security and Authority Boundary

Invented tools inherit no authority. They must pass the same permission checks as pre-registered tools, must not wrap prohibited capabilities, and must be registered with their authority requirements declared. Invention of a tool that circumvents any security boundary is prohibited, not discouraged.

## Evidence

This skill is grounded in dated public implementation references:

1. The Voyager open-ended agent with skill library growth (https://github.com/MineDojo/Voyager).
2. The SkillWeaver self-improving web agent research (https://arxiv.org/abs/2504.07079).

Honest boundary: these are implementation references, not adoption or demand evidence; this entry was added under the owner-directed corpus expansion recorded in `meta/memory/DECISIONS.md`, and no demand signal is claimed for it.

## Related Skills

- [Tool Use Loop](tool-use-loop.md) — the runtime loop that discovers when a primitive is missing.
- [Critic Agent](critic-agent.md) — the review pass every invented tool must survive.

## Changelog

| Date | Version | Change |
|---|---|---|
| `2026-10` | v1 | Initial entry added under the owner-directed corpus expansion |
