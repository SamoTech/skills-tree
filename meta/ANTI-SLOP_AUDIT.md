# Anti-Slop Architecture Audit — 2026-10-03

## Finding

Skills Tree already has strong quality controls for schema validity, runnable examples, tables, stubs, evidence, provenance, security, and unsupported claims. Those controls do not explicitly reject low-information marketing prose or placeholder-style content when a file otherwise passes the maturity checks.

A fresh repository search found no current matches for the selected marketing-filler patterns in canonical skills for:
- seamlessly
- revolutionary
- game-changing

Historical placeholder markers do exist in some canonical skills, including TODO. These are not silently reclassified as new failures by this change.

## Decision

Add a deterministic anti-slop gate that:
- blocks strong placeholder patterns in changed skills;
- blocks selected marketing filler in changed skills;
- reports unsupported absolute claims as warnings;
- reports generic value statements as warnings;
- strips fenced code and frontmatter before prose scanning;
- does not use an LLM to judge style;
- does not alter existing quality classifications.

## Rollout boundary

CI runs the anti-slop gate only against skills changed by a pull request. Existing corpus cleanup is a separate, evidence-driven migration and is not mixed into this architectural gate.

## Non-goals

This gate does not define literary style, ban concise prose, require arbitrary word counts, or treat every adjective as slop. It is not a replacement for schema validation, evidence validation, security scanning, or human review.

## Success criteria

A new skill cannot pass CI while containing deterministic placeholder or selected marketing-filler patterns in its prose. Existing historical content remains unchanged until a dedicated cleanup audit establishes exact remediation scope.
