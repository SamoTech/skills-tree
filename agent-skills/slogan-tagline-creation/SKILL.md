---
name: slogan-tagline-creation
description: Create and evaluate slogans and taglines against brand positioning, memorability, and trademark and clarity constraints, presenting candidates with the reasoning that produced them.
metadata:
  source: skills/13-creative/slogan-tagline-creation.md
  category: 13-creative
  version: "v1"
---

# Slogan and Tagline Creation

Category: Creative | Level: basic | Stability: experimental | Version: v1

## Description

A tagline compresses positioning into a line people can repeat. The skill covers extracting the single claim a tagline must carry from the brand brief, generating candidates through distinct compression strategies, then filtering them: against the positioning, against clarity when read once, against cultural and legal risk, and against distinctiveness from competitors. Output is a shortlist with rationale, not a popularity list.

## When to Use

Use when a product, campaign, or organization needs a short verbal identity line, or an existing one must be refreshed.

Do not pick a winner by taste alone. Without written criteria, the selection measures the room, not the brand.

## Inputs

| Input | Type | Required | Description |
|---|---|---|---|
| `brand_brief` | `object` | Yes | Positioning, audience, and the single claim to compress |
| `constraints` | `object` | No | Length, language, tone, and legal screening limits |
| `count` | `int` | No | Number of candidates to shortlist; defaults to a small set |

## Procedure

1. Extract the one claim the tagline must carry and the audience language for it.
2. Generate candidates through distinct strategies: compression, contrast, and rhythm variants.
3. Filter for clarity: each candidate must be understood correctly on a single hearing.
4. Screen for risk: unintended meanings in other languages and marketplace confusion.
5. Score the survivors against memorability heuristics: brevity, rhythm, and claim fit.
6. Shortlist with rationale attached per candidate and record why the others were cut.

## Outputs

| Output | Type | Description |
|---|---|---|
| `shortlist` | `array` | Candidates with compression strategy and rationale |
| `evaluation` | `table` | Scores on clarity, claim fit, memorability, and risk |
| `screening_notes` | `list` | Cultural and legal screening outcomes |

## Runnable Example

```python
def score_slogans(candidates, weights):
    """candidates: {line: {clarity, fit, memorability}}"""
    out = []
    for line, s in candidates.items():
        total = sum(s[k] * w for k, w in weights.items())
        out.append({"line": line, "score": round(total, 2)})
    return sorted(out, key=lambda x: -x["score"])

print(score_slogans(
    {"Ship faster": {"clarity": 5, "fit": 4, "memorability": 5},
     "Tools for makers": {"clarity": 4, "fit": 5, "memorability": 3}},
    {"clarity": 0.4, "fit": 0.4, "memorability": 0.2},
))
```

## Failure Modes

| Failure Mode | Cause | Mitigation |
|---|---|---|
| Generic line | Claims any competitor could make | Require distinctiveness in the scoring step |
| Winner by taste | No written criteria applied | Score against published dimensions before choosing |
| Unintended reading | No screening beyond the home language | Screen for other-language and slang readings |
| Claim drift | Line outruns what the product does | Anchor every candidate to the extracted claim |
| Legal collision | Similar marks in the same class | Run trademark screening before shortlisting |

## Security and Authority Boundary

Taglines are trademark-sensitive. Run clearance screening before public use, attribute claims honestly so the line cannot misrepresent the product, and treat marketplace confusion findings as a stop condition, not a style preference.

## Evidence

This skill is grounded in dated public implementation references:

1. The Wikipedia article on advertising slogans (https://en.wikipedia.org/wiki/Advertising_slogan).
2. The Wikipedia article on copywriting as a discipline (https://en.wikipedia.org/wiki/Copywriting).

Honest boundary: these are implementation references, not adoption or demand evidence; this entry was added under the owner-directed corpus expansion recorded in `meta/memory/DECISIONS.md`, and no demand signal is claimed for it.

## Related Skills

- [Copywriting](copywriting.md) — the compression craft that taglines push to its limit.
- [Brand Voice Development](brand-voice-development.md) — the voice spec that keeps a short line on-brand when space is tight.

## Changelog

| Date | Version | Change |
|---|---|---|
| `2026-10` | v1 | Initial entry added under the owner-directed corpus expansion |
