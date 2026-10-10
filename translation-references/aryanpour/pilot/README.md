# Aryanpour Phase 3 — Controlled annotation pilot

**Status:** Reproducible pilot implemented and run; source text preserved. Semantic annotation remains **unapproved**.

**Evidence:** [GitHub Actions: pilot + full integrity verification](https://github.com/mohamadadelfa-gif/Translation/actions/runs/38063006821). This run passed 30 regression tests (9 export integrity, 9 markup, 12 pilot tests), the complete 50,259-record corpus inventory, the annotation pilot, and the 45-shard integrity audit.

## 1. Corpus scan and sample

The pilot analyses **50,259** LD2-derived records and selects **94 distinct records** using a deterministic SHA-256 rank within each observation group (up to 12 per group), plus fixed examples and 16 curated source-surface checks. The selected entries are an **evidence and workflow sample**, *not a statistically representative random sample* of lexicographic meanings.

| Text observation class | Records matching (overlapping) |
|---|---:|
| Prefix-group parenthesis beginning with equals sign, e.g. (=abaxile) | 825 |
| A parenthetical with one of the pilot's abbreviation-shaped source strings | 3,721 |
| Other leading parentheticals | 4,986 |
| Embedded parentheticals (not prefix-group) | 4,152 |
| Definitions without parentheses with 3 or more commas | 10,603 |
| Definitions without parentheses with fewer than 3 commas | 27,368 |
| Source-character-damaged definitions/headwords | 3 |
| Unusual headword containing a backtick or parenthesis/angle bracket | 5 |
| Duplicate headword by conservative normalized search key | 2 |

**Important:** These numbers describe *observed surface patterns*, not verified senses, grammatical labels, or cross-references. They overlap, and their total must not be treated as a dictionary entry count. The classes also do not exhaust every unusual printed punctuation pattern, such as the reversed brackets seen in the source export.

## 2. Source-grounded pilot observations

The 16 curated export-surface observations are stored in [reviewed_surfaces.jsonl](reviewed_surfaces.jsonl). Each row pins an exact canonical entry ID, original headword, source field and an **exact source substring**. Generation fails if that substring cannot be found, and no row asserts semantic verification.

| Canonical ID | Original headword | Observed detail | Pilot decision |
|---|---|---|---|
| 3 | a la carte | (در مورد کاغذ) | Textual usage-context candidate; interpretation unverified |
| 4 | aardwolf | (ج. ش.) | Abbreviation-shaped candidate; expansion unverified |
| 12 | aback | ]اسکاتلند[ | Preserve unusual source bracket shape |
| 25 | abasia | ]طب[ | Existing parentheses-only classifier does not capture this bracket form |
| 28 | abate | (حق.) | Embedded parenthesis; scope unresolved |
| 34 | abaxial | (=abaxile) | Exact headword target candidate, not a verified link |
| 35 | abaxile | (=abaxial) | Reciprocal target candidate, not a verified relation |
| 2,176 | apostle | U+FFFD replacement character | Preserve source defect |
| 2,588–2,589 | asafetida / asafoetida | U+FFFD replacement character | Preserve source defects |
| 9,674 | culture | Multiple comma-separated alternatives | No automatic splitting into senses |
| 19,758 | history | Embedded ( طب ) | Do not assign a label scope automatically |
| 30,098 | pace | Multiple comma-separated alternatives | No automatic splitting into senses |
| 36,203 | restoration | Punctuation without a following space | Do not interpret punctuation as a sense break |
| 37,142 | s with unusual literal tokens | Inline source headword tokens | Preserve original headword without silent spelling repair |
| 49,948 | x ray therapy | (طب) | Label-shaped candidate; subject expansion still unverified |

The term "curated" above means **checked against the frozen LD2 export**, including derived readable source text. It does **not** mean checked against an original printed dictionary or approved by a human lexicographer.

## 3. Candidate protocol

1. Read **canonical entry ID + exact original strings**. Retain the SHA-256 digest of the source markup and the existing index shard/anchor.
2. Detect parentheses with explicit [start, end) Unicode string offsets into the original Persian text. The generated record includes the literal matched substring.
3. Classify parenthetical **surface form only** into: apparent reference (text begins with '='), abbreviation-form (known *source string*, with expansion unset), other leading parenthetical, or embedded parenthetical.
4. For apparent references, retain the exact literal target; look up the normalized target in the canonical headword index; retain **zero, one, or multiple candidate IDs**. A unique exact text match is **not** approval of a semantic relationship.
5. Keep confirmed senses, confirmed labels, confirmed references, confirmed examples as **null**. Approved Persian equivalents and translation decisions remain separate.
6. Deterministic sampling covers multiple kinds of unusual input, and includes all three damaged-character records.
7. Run all tests plus the full read-only source integrity audit before accepting a generated pilot artifact.

The pilot **does not** silently correct source text; treat an absent candidate as "not detected by this classifier", not proof that the source has no grammatical label or cross-reference.

## 4. Implementation and generated outputs

- [Pilot builder](../tools/build_annotation_pilot.py) — deterministic corpus scan and review-candidate construction
- [Pilot tests](../tools/test_annotation_pilot.py) — source spans, target ambiguity, non-approval, reproducibility and fail-closed evidence checks
- [Curated source-surface cases](reviewed_surfaces.jsonl) — 16 real records
- [Integrity workflow](https://github.com/mohamadadelfa-gif/Translation/actions/workflows/aryanpour-audit.yml) — automatically creates the pilot summary and sample alongside the Phase 1/2 integrity reports

**Download generated files** from the successful run's "aryanpour-integrity-report" artifact:

- aryanpour-pilot-summary.json — corpus counts, deterministic sample selection IDs, verified source hash
- aryanpour-pilot-sample.jsonl — 94 candidate records with literal source text, string spans, lookup paths, unverified flags and any corresponding export-surface review

The sampled JSONL is a **regenerable CI artifact**, not a replacement for the canonical JSONL. Artifact availability is subject to GitHub retention settings.

Run from repository root, preserving source files:

    python translation-references/aryanpour/tools/build_annotation_pilot.py --root translation-references/aryanpour --output aryanpour-pilot-summary.json --sample aryanpour-pilot-sample.jsonl

## 5. Required research before promoting any semantic rules

- Obtain source-specific documentation explaining the abbreviations and the role of punctuation/brackets in this actual LD2 dictionary or verified print edition.
- Expand the review set to include confusing negatives, multiple embedded parentheses, non-parenthetical labels (such as ]طب[), mismatched source headwords and references with missing/duplicate exact targets.
- Use an independently reviewed ground-truth corpus and **evaluate precision/recall by candidate type**, with explicit scope, reviewer, evidence and review date.
- Never normalize headwords or Persian definitions in the canonical export, never combine same-spelled entry IDs, and never merge Aryanpour entries into a translator-approved glossary without a separate decision.

**Phase 3 outcome:** reproducible **candidate detection and evidence review** demonstrated. **Automatic semantic dictionary parsing is not validated**. The next stage should evaluate a carefully reviewed abbreviation/reference convention register before enabling semantic labels or links.
