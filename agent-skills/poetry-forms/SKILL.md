---
name: poetry-forms
description: Write within fixed poetic forms by checking their mechanical constraints — syllable counts, line counts, rhyme schemes — so form compliance is verified rather than asserted.
metadata:
  source: skills/13-creative/poetry-forms.md
  category: 13-creative
  version: "v1"
---

# Poetry Forms

Category: Creative | Level: basic | Stability: experimental | Version: v1

## Description

A fixed form is a contract in counts: five and seven for the haiku, fourteen lines with a rhyme scheme for the sonnet. Meeting the contract by assertion is how “approximate haiku” happens. This skill treats form compliance as checkable arithmetic — per-line syllable counts against declared targets, line count against the form, rhyme pattern against the scheme — with the checks running before the poem is presented as done.

## When to Use

Use when writing in a fixed form, when an exercise or publication requires exact form compliance, or when teaching forms where the mechanics matter.

Do not use for free verse; imposing fixed-form checks on open forms misreads the contract.

## Inputs

| Input | Type | Required | Description |
|---|---|---|---|
| `lines` | `list[string]` | Yes | The poem’s lines in order |
| `form` | `map[field -> value]` | Yes | Declared constraints: syllables, line count, rhyme scheme |

## Procedure

1. Declare the form’s numeric contract up front — syllable targets per line, line count, rhyme scheme.
2. Count syllables per line with a stated counting convention, and record the count next to each line.
3. Check line count against the form before deeper checks; wrong length is the first failure.
4. Map rhyme classes per line and compare the resulting pattern against the declared scheme.
5. Report every deviation with the offending line rather than a bare failure flag.
6. Revise the line, not the check; weakening the contract to pass is self-deception.

## Outputs

| Output | Type | Description |
|---|---|---|
| `counts` | `list[integer]` | Syllable count per line, in order |
| `deviations` | `list[(line_index, expected, actual)]` | Lines violating the declared form |

## Runnable Example

```python
def count_syllables(line, vowels="aeiouy"):
    """Heuristic vowel-run syllable counter for checking drafts."""
    count, previous_vowel = 0, False
    for ch in line.lower():
        is_vowel = ch in vowels
        if is_vowel and not previous_vowel:
            count += 1
        previous_vowel = is_vowel
    return count

def check_form(lines, targets):
    deviations = []
    counts = [count_syllables(line) for line in lines]
    for i, (count, target) in enumerate(zip(counts, targets), 1):
        if count != target:
            deviations.append((i, target, count))
    return counts, deviations

haiku = ["an old silent pond", "a frog jumps into the pond", "the sound of water"]
counts, deviations = check_form(haiku, [5, 7, 5])
print("counts:", counts, "deviations:", deviations)
```

## Failure Modes

| Failure Mode | Cause | Mitigation |
|---|---|---|
| Approximate form | Counts asserted without checking | Run the arithmetic and record per-line counts |
| Heuristic overtrust | Vowel-run counter treated as ground truth | Flag heuristic counts for human review on hard cases |
| Contract weakening | Targets edited to fit the draft | Revise the line, not the declared form |
| Scheme drift | Rhyme pattern left unchecked | Map the realized scheme against the declared one |
| Form confusion | Free verse judged by fixed-form rules | Match the checks to the declared form |

## Security and Authority Boundary

Form constraints govern counts and sound, not appropriation. Diction borrowed from living traditions carries the same research and respect obligations as any cultural material, regardless of syllable totals.

## Evidence

This skill is grounded in dated public implementation references:

1. Wikipedia’s overview of the haiku and its syllable convention (https://en.wikipedia.org/wiki/Haiku).
2. Wikipedia’s overview of the sonnet form (https://en.wikipedia.org/wiki/Sonnet).

Honest boundary: these are implementation references, not adoption or demand evidence; this entry was added under the owner-directed corpus expansion recorded in `meta/memory/DECISIONS.md`, and no demand signal is claimed for it.

## Related Skills

- [Lyrics Writing](lyrics-writing.md) — musical writing that borrows these counting and rhyme contracts.
- [Creative Writing](creative-writing.md) — the broader prose and verse craft this skill formalizes for fixed forms.

## Changelog

| Date | Version | Change |
|---|---|---|
| `2026-10` | v1 | Initial entry added under the owner-directed corpus expansion |
