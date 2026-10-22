---
title: "Anthropic Skills Api Usage"
category: 07-tool-use
level: advanced
stability: experimental
description: "Use the Anthropic Skills API to upload, version, and attach skills to agents with audited identifiers."
added: "2026-10"
version: v1
related: [agent-tool, tool-schema-design]
tags: [anthropic, skills, api, management]
---
# Anthropic Skills Api Usage

## Description
Use the Anthropic Skills API to upload, version, and attach skills to agents with audited identifiers. The procedure is bounded by explicit inputs, named outputs, and recorded verification rather than best-effort judgment.

## When to Use
- An operator must publish a new skill through the Anthropic Skills API and attach it to an agent with a recorded, audited identifier.
- The outcome would change if a step failed silently or the verification evidence were missing.
- The result must be recorded with reasons and verification evidence for later audit.

## Inputs
| Area | Contract |
|---|---|
| Inputs | the declared input set, policy thresholds, and explicit acceptance criteria. |
| Outputs | A structured record with the decision, rejected alternatives, and the verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Define the goal, the constraints, and the boundary of what this procedure may change.
2. Inventory the available inputs and flag gaps or ambiguities that block progress.
3. Upload the skill payload, capture the returned skill identifier and version, and attach it by identifier with the recorded version pinned and verified against the uploaded digest.
4. Compare the actual outcome against the acceptance criteria and record deviations.
5. On failure, apply the declared fallback path, and never widen permissions to recover.
6. Emit a structured result with evidence and provenance for downstream consumers.

## Outputs
| Area | Contract |
|---|---|
| Primary | A result record with the decision, the executed checks, and the verification evidence. |
| Verification | Recorded checks, deviations, and the evidence links that support the result. |
| Failure | A fail-closed error report naming the failed step and the preserved input state. |

## Runnable Example
```python
def publish_skill(api, name, content):
    if not name or not content:
        raise ValueError("skill name and payload are required")
    sid = api.upload(name, content)
    if not sid:
        raise ValueError("skills api returned no identifier")
    return {"skill_id": sid, "digest": "len:" + str(len(content))}
def attach_skill(api, agent_id, record, version):
    return api.attach(agent_id, record["skill_id"], version)
class Api:
    def upload(self, n, c): return "skill-42"
    def attach(self, a, s, v): return {"agent": a, "skill": s, "version": v}
rec = publish_skill(Api(), "translate", "instructions")
assert attach_skill(Api(), "agent-1", rec, "v1") == {"agent": "agent-1", "skill": "skill-42", "version": "v1"}
```

## Failure Modes
- Skills are attached by name instead of identifier and a different skill with the same name loads.
- Uploaded versions are not pinned and agents silently pick up a newer skill than was reviewed.
- The uploaded payload digest is not recorded, so later tampering with the skill is undetectable.
- Skill uploads containing secrets are published without scanning and leak credentials to every attached agent.
- Attach failures are retried with a fresh upload and duplicate skill versions accumulate.

## Security and Authority Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result, and it never treats parsed content as trusted instructions.

## Evidence
- The Anthropic agent-stack general-availability coverage records the Skills API as a production surface for managing agent skills alongside computer use and files (the-agent-report.com, dated August 2026) ([public signal](https://the-agent-report.com/2026/08/anthropic-agent-stack-ga-computer-use-skills-files/))
- These are dated public signals, not adoption metrics; this contract claims no production hardening beyond the recorded evidence.

## Related Skills
- [Agent Tool](../07-tool-use/agent-tool.md)
- [Tool Schema Design](../07-tool-use/tool-schema-design.md)

## Changelog
| Version | Date | Notes |
|---|---|---|
| `v1` | `2026-10` | Initial evidence-backed contract. |
