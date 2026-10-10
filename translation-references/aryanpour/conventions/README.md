# Aryanpour Phase 4 — Convention evidence register and audit

**Status: evidence gathering and automated candidate inventory implemented; lexicographic conventions NOT YET APPROVED.**

Phase 4 investigates what surface forms in the frozen Aryanpour LD2 export *might* mean. The original dictionary records, index and translation choices remain unchanged.

## Evidence hierarchy

1. **Frozen LD2 export:** the 50,259 canonical `id` records, exact `english` and `persian` text and unmodified `original_definition_markup`. Supports literal observations only.
2. **Independent source-specific lexicographic documentation:** original printed edition title/copyright and its abbreviation/index/explanatory key, or verifiably edition-matched source handbook. **Not yet located or authenticated.** Required to approve abbreviation expansions and interpret ambiguous signs.
3. **Current Aryanpour website** ([about](https://aryanpour.com/about.php); [English-to-Persian examples](https://www.aryanpour.com/Aryanpour-Farsi-Dictionary.php)): useful *external comparator* with superficially similar headwords and abbreviations. **Not proof that this legacy LD2 dump is identical to the website's current data or an identified printed edition**; it may have different entries, descriptions and punctuation.
4. **Editorial inference:** hypothesis only until supported with source-specific evidence.

In the absence of layer 2, the software **MUST NOT** certify any label meaning, scope, part of speech, cross-reference relation, or lexical sense boundary.

## Files

- [register.jsonl](register.jsonl): 11 literal source-anchored evidence cases. Each row has `rule_id`, `candidate_class`, `surface_key`, `canonical_id`, `source_field`, `source_text`, `evidence_grade`, `source_documentation_status`, `editorial_status`, and **null semantic fields**.
- [audit_conventions.py](../tools/audit_conventions.py): full-corpus read-only audit of simple enclosed-text forms. Retains exact offsets, source literals, bracket shapes, reference target literals and all exact normalized headword matches, including missing or ambiguous matches.
- [test_audit_conventions.py](../tools/test_audit_conventions.py): rejects absent source spans, false semantic approvals, wrong register comparisons and spurious reference matches.
- The existing [Phase 3 pilot](../pilot/README.md) remains separate, with 94 review items and 16 export-surface checked examples.
- [GitHub Actions](https://github.com/mohamadadelfa-gif/Translation/actions/workflows/aryanpour-audit.yml) saves the Phase 4 JSON summary and candidate JSONL with all prior integrity reports.

## Distinctions enforced

| Observed text | Source item | What the audit CAN report | What it CANNOT certify |
|---|---|---|---|
| `(طب)` | `x ray therapy`, ID 49948 | Exact parenthetical abbreviation-shaped occurrence | Expansion and domain-label scope |
| `(ج. ش.)` | `aardwolf`, ID 4 | Exact parenthetical surface | Meaning of this abbreviation |
| `(گ . ش.)` | `abaxial`, ID 34 | Whitespace-insensitive comparison key | Normalized rewrite of source; domain certainty |
| `(حق.)` | `abate`, ID 28 | Embedded parenthetical substring | Whether it qualifies all or only later equivalents |
| `(=abaxile)` | `abaxial`, ID 34 | Apparent equals-marker + candidate target literal, matched against headwords | Authenticated *see also* relation |
| `(=abaxial)` | `abaxile`, ID 35 | Reciprocal candidate match | Approved bidirectional lexical relation |
| `(در مورد کاغذ)` | `a la carte`, ID 3 | Enclosed usage-context wording | Grammatical category |
| `]طب[` | `abasia`, ID 25 | Mirrored-square-bracket **string form** | Original print bracket orientation, scope or semantics |
| `]اسکاتلند[` | `aback`, ID 12 | Mirrored-square-bracket **string form** | Label vs context vs rendering defect |
| `( طب )` | `history`, ID 19758 | Embedded source text | Independently established sense segmentation |

The current audit detects simple parentheses, normal square brackets and mirrored square brackets as **separate forms**. It detects equals signs both *before* and *after* a candidate target (RTL rendering can affect apparent ordering). An equals sign at both ends is flagged ambiguous, not silently interpreted.

### Review and promotion rule

**Source observation** `→` **candidate classification** `→` **independent evidence** `→` **human-reviewed decision** `→` **semantic rule only if justified**.

The first two stages are automated; the last three are **not**. Status `unverified` means *do not use as authoritative semantics*.

A pilot parser's exact headword match is a **navigation result**, not proof of a lexicographic relationship. Multiple same-key source IDs must all be exposed; missing targets must remain missing. Source replacements (U+FFFD) are not silently repaired.

### How to run

From repository root:

```powershell
python translation-references/aryanpour/tools/audit_conventions.py --root translation-references/aryanpour --report aryanpour-convention-audit.json --candidates aryanpour-convention-candidates.jsonl
```

The candidate JSONL is potentially large and is generated as a **CI artifact** rather than committed over source data. The summary reports raw counts of syntactic observations and reference-target lookup outcomes, not verified linguistic annotations. Corpus counts can overlap and must not be treated as proportions of accepted meanings.

### Next validation gate

1. Locate a verified edition-specific abbreviation/typographic key, *or explicitly document its absence*; avoid substituting an unrelated dictionary's conventions.
2. Human-label a stratified corpus with positives **and confusing negatives**, using evidence offsets and the original full definitions.
3. Review confusing examples such as `(abaxile=)`, `(=abaxile)`, `(حق.)` embedded in a multiple-equivalent entry, `]طب[` and non-abbreviated `(در مورد کاغذ)`.
4. Evaluate precision **and recall** separately for bracket-class detection, apparent-reference candidates and potential grammatical/domain labels. Abbreviation expansion/scope requires verified source guidance.
5. Only *then* add a semantically enriched **separate overlay**; do not change canonical Aryanpour, merge entry IDs, or approve translator-selected equivalents automatically.

**No approved semantics in this phase**. A passing workflow certifies that the source evidence and candidate extraction are consistent, not that the proposed roles have been established.
