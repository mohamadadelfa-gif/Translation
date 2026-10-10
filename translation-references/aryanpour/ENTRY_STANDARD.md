# Aryanpour Entry Standard — Phase 1 (draft)

**Status:** Implementation draft; structural assumptions pending full-corpus audit. **Scope:** the Aryanpour English–Persian dictionary export in `translation-references/aryanpour/` of the Translation repository. This is **not** an OCR workflow and does not certify the attribution or print edition.

## 1. Authority hierarchy

1. Frozen `.ld2` dictionary bytes (when independently available); conversion report records the source SHA-256 (`d69ee28c3faa54648528e754aef85cb51f62f6330c0cadeed943ae2c5984d765`).
2. Canonical `aryanpour-english-persian.jsonl`, derived from those bytes, as source of record for normal lookups. Its hash is recorded in `manifest.json`.
3. `aryanpour-english-persian.txt` is a readable projection.
4. `dictionary/[letter]/[shard].md` and `index/*` are **derived retrieval artifacts**, never the authority for reconstruction.
5. Context-sensitive translation choices and glossary approvals are a separate editorial layer, not dictionary content.

Do not amend the canonical file to correct suspected defects. Corrections and annotations belong in a distinct reviewed overlay with the canonical entry ID and cited evidence.

## 2. Canonical source contract (existing, do not migrate)

Each source JSONL record has these observed keys:

```json
{
  "id": 49948,
  "english": "x ray therapy",
  "persian": "(طب) درمان  با اشعه  مجهول.",
  "original_definition_markup": "<the original LD2 definition markup, verbatim>",
  "source_character_issue": false
}
```

**Important:** The sample `original_definition_markup` string above is a descriptive placeholder, not a transcribed value. Source markup could not be sampled from the full canonical export through the connected file interface; verified examples of markup were available in `source-character-issues.json`.

The existing export routine computes `persian` from `original_definition_markup` by converting `<n/>` tags to newlines, then removing other angle-bracket tags. `persian` is thus a readable projection, **not** proof that the markup has been semantically interpreted. Exact spacing, punctuation, Persian orthography, and source-character damage must be retained.

## 3. Optional derived entry wrapper

An enhanced index can wrap an **unaltered** canonical record without duplicating or replacing canonical data:

```json
{
  "schema_version": "aryanpour.entry.v1",
  "source": {
    "type": "structured_ld2",
    "dictionary": "aryanpour",
    "canonical_record_id": 49948,
    "canonical_path": "translation-references/aryanpour/aryanpour-english-persian.jsonl"
  },
  "lookup": {
    "headword_original": "x ray therapy",
    "headword_normalized": "x ray therapy",
    "shard_path": "dictionary/X/X-01.md",
    "anchor": "entry-49948-x-ray-therapy"
  },
  "observations": {
    "domain_label_candidates": ["طب"],
    "sense_boundaries": null,
    "candidate_notes": ["Parenthesized label appears before Persian equivalents; classification remains provisional."]
  },
  "verification": {
    "source_export_integrity": "reported_passed",
    "dictionary_print_edition": "not_independently_verified",
    "sense_segmentation": "not_verified",
    "editorial_translation_approval": false
  }
}
```

The `lookup` layer **may** normalize an English headword only for navigation. Candidate labels, relationships, and sense boundaries are hypotheses until justified by source markup or dictionary conventions. Never claim that all comma-separated equivalents are separate senses.

## 4. Preservation rules

- `id` is the permanent reference key **for this frozen export**; do not merge duplicate headwords by string.
- Preserve `english`, `persian`, `original_definition_markup`, and `source_character_issue` verbatim.
- No inferred page numbers or OCR bounding boxes: this source is not page OCR.
- Keep all potentially meaningful marks (`(طب)`, parentheses, unusual characters, source misspellings).
- Do not treat parentheses as automatic cross-references or domain labels.
- Preserve all existing source issues (`apostle` ID 2176, `asafetida` ID 2588, `asafoetida` ID 2589). Do not silently replace U+FFFD.
- Apply Unicode NFKC / whitespace collapse / case folding only to explicit search keys.
- Do not select the first listed Persian equivalent by default. Translation choice requires context and a separate decision record.
- Never treat a passing checksum/decoding audit as proof that the edition attribution, individual definitions, or sense splits are correct.

## 5. Required read-only checks

1. SHA-256 digests of all manifest-listed source/export files match the frozen manifest.
2. All JSONL rows parse; IDs are unique and consecutive from 1 through 50,259.
3. Required fields have appropriate types; projection of markup matches `persian` exactly under the original converter's transformation.
4. U+FFFD detection and `source_character_issue` flags agree.
5. Every record ID occurs in the navigation index exactly once and points to a consistent headword, normalized form, issue flag, shard path, and anchor.
6. Counts per letter and shard count match the manifest; index points to actual Markdown anchors when full shard checking is enabled.
7. Same exact headword stays together in one shard; different source IDs remain distinct.
8. Audit emits actionable failures and never writes back to the dictionary.

### Run the pilot validator

Put `audit_aryanpour.py` in `translation-references/aryanpour/tools/` (or run it with an explicit root), then run:

```powershell
python translation-references/aryanpour/tools/audit_aryanpour.py --root translation-references/aryanpour --check-shards --output aryanpour-audit.json
```

The auditor tests repository integrity, **not** lexicographic quality. A full-repository GitHub Actions audit must pass before promoting this standard from draft.

## 6. Pilot evidence sampled through GitHub

| Source record | Observation | Action |
|---|---|---|
| `pace` (ID 30098) | Multiple Persian equivalents and usage phrase in one unsegmented definition | Keep original definition atomic; do not create fabricated numbered senses |
| `aback` (ID 12) | Unusual `]اسکاتلند[` punctuation | Preserve verbatim; optional editorial note |
| `cabbala` (ID 5685) | Parenthesized English spelling variants | Do not assert machine-parsed cross-reference without verification |
| `x ray therapy` (ID 49948) | Leading `(طب)` | Candidate domain label only |
| `s … words … man` (ID 37142) | Anomalous headword tokens/markup presentation in shard | Flag for source-level check; never silently correct |
| `apostle` (ID 2176) | U+FFFD in Persian source text | Preserve as source-character issue |

## 7. Remaining work before full acceptance

- Run `audit_aryanpour.py` against all canonical files in a local checkout, with `--check-shards`.
- Inspect original markup for representative records across grammar labels, multiple senses, examples, variants, and referrals before specifying any semantic parser.
- Review whether the source edition can be independently attributed. Current original source is a generic Lingoes `.ld2` and the repository explicitly says attribution was user supplied.
- Only then add an optional enriched-record generator, leaving the canonical JSONL untouched.
## 8. Automated verification

`.github/workflows/aryanpour-audit.yml` runs the regression tests and a read-only whole-corpus audit on relevant changes or manual dispatch. Its audit JSON artifact is an integrity report, **not** approval of lexicographic content or translation choices.
