# Aryanpour Phase 4 — Initial corpus audit results

**Completed audit:** [GitHub Actions run 38075055800](https://github.com/mohamadadelfa-gif/Translation/actions/runs/38075055800), on commit `50b2b5760e6a05e1836a878881d86c170284aae8`. Results from the unchanged 50,259-record export. **No semantics are approved.**

## Findings

| Syntactic candidate type | Occurrences |
|---|---:|
| All detected simple enclosed-text candidates | 14,576 |
| Parentheses | 14,550 |
| Mirrored square brackets, e.g. `]طب[` | 23 |
| Standard square brackets | 3 |
| Apparent equals-marked references (either equals position) | 950 |
| Registered abbreviation-shaped parentheticals | 2,920 |
| Unclassified enclosed-text surfaces | 10,683 |
| Enclosed candidates participating in overlapping spans | 6 |

Reference-target lookup results (**surface syntax only**):

| Candidate syntax / lookup outcome | Occurrences |
|---|---:|
| `(=headword)`, exact target found once | 695 |
| `(=headword)`, no exact target | 165 |
| `(headword=)`, exact target found once | 45 |
| `(headword=)`, no exact target | 45 |
| **Total** | **950** |

All totals count **occurrences**, not distinct entries or verified dictionaries' senses; some categories overlap. The 2,920 abbreviation candidates are the **forms registered for conservative matching** in this pilot, not the universe of all possible abbreviations.

### What is now reliable

- Candidate literals and [start, end) offsets point back into unchanged canonical Persian definitions.
- Exactly matching a reference target looks up **all** canonical IDs with a matching search key, preserving ambiguity and missing targets.
- The audit detects parentheses, ordinary square brackets and reversed square brackets, and flags overlapping spans instead of selecting a fake parse.
- The 11 [register entries](register.jsonl) are all supported by literal source substrings and have **unverified** interpretation status.
- Source corruption is retained: neither the 3 replacement-character records nor odd punctuation is repaired.

### What remains unverified

- Identity of the actual printed dictionary edition underlying this legacy LD2 export.
- The publisher/edition's abbreviation guide and conventions.
- Whether a token such as `ج. ش.` has one domain expansion or multiple context-specific readings.
- Scope of embedded labels (especially after several comma-separated equivalents).
- Whether equals-marked surface forms indicate variants, synonyms, compare-to, or another relation.
- Whether punctuation ever reliably distinguishes individual dictionary senses.

External comparison: the [currently published Aryanpour website](https://www.aryanpour.com/Aryanpour-Farsi-Dictionary.php) exhibits similar surface notation, but it is **not established to be the same edition/data**. It does not substitute for the original abbreviations guide.

## Reproduction and sign-off criteria

The complete audit report and literal candidate JSONL are attached to [the successful workflow](https://github.com/mohamadadelfa-gif/Translation/actions/runs/38075055800) as part of `aryanpour-integrity-report`. Source corpus and index integrity continue to be validated by the same workflow.

**Current release gate:** no semantic promotion until a relevant original-edition guide is verified and a separately adjudicated gold-standard sample supports precision/recall evaluation. Exact-headword linking is a candidate retrieval operation, *not* a semantic verdict. Count of approved conventions: **0**.
