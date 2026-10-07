# Repository Structural Audit — Post-Repair Verification

**Date:** 2026-10-07  
**Repository:** `mohamadadelfa-gif/Translation`  
**Branch:** `master`

This report closes the structural repair cycle initiated by `archive/audits/2026-10-07-structural-audit.md`.

## Verification result

GitHub Actions workflow:

- Workflow: `Repository structural audit`
- Run ID: `37620112758`
- Trigger commit: `558f21811f432c486adf683e800c8fe1e8f9e3b9`
- Job: `structural-audit`
- Step: `Run structural audit`
- Result: **success**
- Runner: Ubuntu / Python 3.12

This is a fresh GitHub checkout, so the validator ran against the tracked repository rather than a local working copy.

## Closed structural defects

### Workflow authority

- `MENTOR_WORKFLOW.md` is the single authoritative workflow.
- The nonexistent `translation-references/TRANSLATION-PROFILE.md` dependency was removed.
- The Najafi lookup path is canonical: `translation-references/najafi/tools/najafi_lookup.py`.
- `AGENTS.md` is now a short operational entrypoint.
- Hezareh match semantics and other source-specific retrieval facts live in `SOURCE-REGISTER.md`.
- The old workflow-like tail in `SOURCE-REGISTER.md` was removed.
- `WORD-CHOICE-POLICY.md` remains only as a compatibility pointer.

### Practice Chunk state

Authoritative chunk map:

`translation-preparation/PRACTICE-CHUNKS.json`

Verified active boundaries:

- `C01-S01-P01`: **338 source words**
  - starts with the Kristijana Gunnars epigraph;
  - ends with Thomas Mann: “Humanity shudders in horror at Germany!”
- `C01-S01-P02`: **254 source words**
  - starts with “The elderly Mann...”;
  - ends with the Franz Werfel block quotation.

The anchors in the map match the boundaries encoded in `translation-preparation/C01.md`.

`PROGRESS.md` now records `C01-S01-P02` as the current Practice Chunk and the next canonical save path as:

`drafts/C01/C01-S01-P02-draft-01.md`

Existing `C01-S01-opening-*` files remain historical filenames mapped to P01 and are not renamed cosmetically.

### Source / working layers

- No Practice Chunk markers are present in `sources/`.
- New structural annotations remain in `translation-preparation/`.
- `tools/organize.ps1` defaults to the tracked frozen structured snapshot, strips known working markers in memory, and reapplies established Practice Chunks from `PRACTICE-CHUNKS.json`.
- Regeneration fails if a recorded Practice Chunk start/end anchor cannot be found.

### Primary-book provenance

The original supplied PDF was recovered from Adel's persistent file library and visually identified.

Recorded in:

`translation-references/SOURCE-PROVENANCE.md`

Verified properties:

- 115 pages
- 330735 bytes
- SHA-256: `0efedab3987f2dc797db4b5f10c290215e06556a39239097065f927fcef2f0be`
- cover identity visually checked

The PDF is the canonical visual authority.

### Draft / approval layout

Drafts are chapter-scoped:

`drafts/Cxx/`

Approved translations are defined symmetrically:

`approved-translations/Cxx/Cxx-Sxx-Pxx-approved.md`

There are currently **0 approved translation files**, so no unapproved text has entered the approval layer.

### Translation-craft corpus

Current location:

`translation-references/translation-craft/corpus/`

Move verification against the pre-move tree:

- pre-move corpus files: **139**
- missing after move: **0**
- files with changed Git blob SHA: **4**
- the four changed files are metadata/path files only:
  - `README.md`
  - `paired-sections.csv`
  - `paired-sections.jsonl`
  - `source-manifest.json`
- all section-content blobs remained unchanged
- aligned rows: **59**
- section file references: **118**
- duplicate section references: **0**
- unresolved section references: **0**

The corpus's own validator is also executed by `tools/audit_repository.py` in CI.

### Tool reproducibility

`tools/organize.ps1`

- no hard-coded Adel Desktop input;
- repository-default source;
- optional `-SourcePath` / `ZERO_HOUR_SOURCE_MD`;
- deterministic Practice Chunk reapplication.

`tools/test-dictionary.cjs`

- no hard-coded Adel Desktop input;
- requires `--source <path>` or `ARYANPOUR_LD2_PATH`;
- enforces Ariyanpour LD2 SHA-256:
  `d69ee28c3faa54648528e754aef85cb51f62f6330c0cadeed943ae2c5984d765`.

## Link and reference-system checks

Final active-link scan:

- internal Markdown links checked: **64**
- broken internal links: **0**

Reference subsystem wiring verified for:

- Ariyanpour
- Hezareh
- Ashouri
- Najafi
- Persian thesaurus
- Academy orthography
- Huddleston/Pullum/Reynolds grammar layer
- Daryabandari/Faulkner translation-craft layer

## Remaining bounded warnings

### 1. Original book PDF is not yet binary-tracked in GitHub

**Status:** bounded external-storage warning, not a provenance ambiguity.

The exact PDF has been recovered, visually checked, and checksum-registered, but the current connected GitHub write interface cannot safely copy binary bytes into the repository.

Do not claim that the binary is in GitHub until a byte-identical copy with the recorded SHA-256 is actually added.

The source remains recoverable from Adel's persistent file library for page-level verification.

### 2. Eleven historical draft artifacts retain legacy filenames

**Status:** accepted historical state.

They remain chapter-scoped and are preserved for traceability. New saved work must use `Cxx-Sxx-Pxx` filenames. The validator treats these existing files as warnings rather than silently renaming them.

## Enforcement

Permanent validator:

`tools/audit_repository.py`

CI workflow:

`.github/workflows/structural-audit.yml`

The validator now runs automatically on:

- every push to `master`;
- every pull request.

A structural failure produces a failing CI job.

## Final audit state

**Structural failures: 0**

The repository is now stable enough to resume C01 translation under the declared pipeline:

```text
frozen source / canonical evidence
→ translation-preparation
→ Practice Chunk
→ Adel draft
→ mentor review
→ evidence gate
→ Adel approval
→ approved-translations
```

Current active location:

`C01-S01-P02`
