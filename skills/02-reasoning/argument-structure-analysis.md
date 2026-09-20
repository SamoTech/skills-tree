---
title: "Argument Structure Analysis"
category: 02-reasoning
level: intermediate
stability: stable
description: "Decompose arguments into premises, conclusions, inference links, and explicit gaps so agents distinguish stated evidence from unsupported claims."
added: "2025-03"
version: v2
related: [deductive-reasoning, inductive-reasoning, ../06-communication/citation-attribution]
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-02-reasoning-argument-structure-analysis.json)

# Argument Structure Analysis
Category: reasoning | Level: intermediate | Stability: stable | Version: v2

## Description
Argument structure analysis represents an argument as claims connected by stated or inferred support.
The core task is decomposition: identify premises, a conclusion, the relation between them, and missing assumptions.
Fallacy detection is a separate judgment and should not be treated as a guaranteed output of parsing.

## Inputs / Outputs
| Input | Type | Contract |
|---|---|---|
| `text` | `str` | Bounded natural-language argument |
| `premises` | `list[str]` | Optional manually extracted premise candidates |
| `conclusion` | `str | None` | Optional explicit conclusion |

| Output | Type | Contract |
|---|---|---|
| `premises` | `list[str]` | Ordered claims offered as support |
| `conclusion` | `str | None` | Best-supported conclusion or null |
| `gaps` | `list[str]` | Explicitly stated missing assumptions; never invented as facts |
| `relations` | `list[dict]` | Support links between claims |

## Deterministic Reference Implementation
```python
import re


def split_argument(text):
    if not isinstance(text, str) or not text.strip():
        raise ValueError("text must be a non-empty string")
    parts = [p.strip() for p in re.split(r"(?<=[.!?])\s+", text.strip()) if p.strip()]
    conclusion = None
    premises = parts[:]
    for index, part in enumerate(parts):
        if re.search(r"\b(therefore|thus|hence|so)\b", part, re.I):
            conclusion = re.sub(r"^.*?\b(therefore|thus|hence|so)\b\s*", "", part, flags=re.I)
            premises = parts[:index] + parts[index + 1:]
            break
    return {
        "premises": premises,
        "conclusion": conclusion,
        "gaps": [],
        "relations": [{"from": p, "to": conclusion, "type": "supports"}
                       for p in premises] if conclusion else [],
    }

result = split_argument("All mammals are warm-blooded. Whales are mammals. Therefore whales are warm-blooded.")
assert result["conclusion"] == "whales are warm-blooded."
```

## Analysis Protocol
1. Preserve the original wording before normalization.
2. Separate explicit premises from conclusions.
3. Record inference markers without treating them as proof.
4. Mark missing assumptions as hypotheses, not recovered facts.
5. Distinguish logical validity from factual truth.
6. Evaluate fallacies only after the argument structure is explicit.

## Failure Modes
| Cause | Observable result | Mitigation |
|---|---|---|
| Implicit premise | Gap in support chain | Label the missing premise explicitly |
| Circular reasoning | Conclusion appears in its own support | Check dependency paths for cycles |
| Ambiguous pronoun | Unclear claim reference | Preserve ambiguity rather than guessing |
| Multiple conclusions | Flat extraction loses hierarchy | Build separate conclusion nodes |
| Rhetorical language | False premise detection | Separate rhetoric from propositional content |

## Validation Rules
- Every relation must reference an existing claim.
- No missing assumption may be represented as an observed fact.
- A conclusion is not automatically valid because it follows an indicator word.
- Factual verification is outside the structural parser's boundary.
- The same input must produce the same deterministic parse under the reference implementation.

## Safety Boundaries
Do not infer criminal intent, medical diagnosis, legal liability, or other high-impact attributes from argument structure alone.
When an argument contains sensitive claims, preserve attribution and uncertainty and require domain-specific review for consequential decisions.

## Provenance
The deterministic example is a structural baseline, not an LLM reasoning benchmark.
LLM-based extraction can be layered on top, but its claims require independent validation and source attribution.

## Related
- `deductive-reasoning.md` — validity of deductive forms
- `inductive-reasoning.md` — strength of generalization
- `../06-communication/citation-attribution` — evidence attribution

## Changelog
- v1 (2026-04): Initial entry
- v2 (2026-09-20): Added deterministic structural parser, typed I/O, validation rules, failure modes, provenance, and safety boundaries
