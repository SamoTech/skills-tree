---
title: "Social Media Post"
category: 13-creative
level: advanced
stability: stable
version: v2
added: "2025-03"
updated: "2026-10-03"
description: "Create platform-specific social posts from a source brief while preserving factual claims, audience constraints, character limits, and disclosure requirements."
---

# Social Media Post

## Purpose

Transform a source brief into platform-specific post drafts. Platform formatting is an output constraint; it is not permission to invent facts or engagement claims.

## Inputs / Outputs

| Item | Type | Required | Notes |
|---|---|---:|---|
| Source brief | str | yes | Facts and intended message |
| Platform | enum | yes | Target channel |
| Audience | str | yes | Intended audience |
| Tone | str | no | Optional style constraint |
| Post | str | yes | Platform-specific draft |
| Claims | list[str] | recommended | Claims that should remain traceable |

## Runnable Example

```python
from dataclasses import dataclass

@dataclass
class PostRequest:
    platform: str
    topic: str
    facts: list[str]
    call_to_action: str = ""

def draft(req: PostRequest) -> str:
    body = f"{req.topic}\n\n" + "\n".join(f"• {fact}" for fact in req.facts)
    if req.call_to_action:
        body += f"\n\n{req.call_to_action}"
    return body

request = PostRequest(
    platform="linkedin",
    topic="Why evidence-backed AI skills matter",
    facts=["Claims should remain traceable to sources.", "Generated content should distinguish evidence from inference."],
    call_to_action="Read the source documentation.",
)
print(draft(request))
```

## Platform Adaptation

- Treat each platform's current published limits as external constraints; verify them before automated publishing.
- Preserve the source brief as provenance.
- Keep sponsorship, affiliate, or promotional disclosures when required.
- Do not fabricate social proof, customer numbers, engagement rates, or urgency.
- Separate draft generation from publishing authorization.

## Failure Modes

| Failure | Cause | Mitigation |
|---|---|---|
| Unsupported claim | Source brief lacks evidence | Remove, qualify, or source the claim |
| Wrong platform format | Constraints changed | Validate against current platform rules before publishing |
| Accidental publication | Generation and publishing are coupled | Require an explicit publishing boundary |
| Disclosure omission | Commercial context is hidden | Carry disclosure metadata with the draft |

## Evidence

Platform limits and policies change. This skill therefore treats them as runtime inputs rather than hard-coded facts.

Evidence status: no engagement or conversion claim is made.

## Related Skills

- copywriting
- tone-adjustment
- structured-output

## Changelog

| Version | Date | Change |
|---|---|---|
| v1 | 2025-03 | Initial entry |
| v2 | 2026-10 | Added source-bound claims, publishing boundary, and deterministic example |
