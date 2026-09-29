# Hezareh model retrieval layer

This directory is a derived, GitHub-friendly retrieval layer for the Hezareh dictionary package.

## Canonical source

The canonical/extraction package remains unchanged under:

`sources/Hezareh_Dictionary_Index/`

This derived layer belongs under:

`translation-references/hezareh/`

## Build summary

- Records: 38,957
- Shards: 174
- Target shard size: ~250,000 UTF-8 bytes
- Largest shard: 250,385 bytes
- `visually_checked`: 186
- `raw_ocr`: 38,771
- `high` boundary confidence: 17,933
- `medium`: 13,719
- `low`: 2,658
- `hint_only`: 4,647

## Routine lookup

1. Open `index/<LETTER>-headwords.csv`.
2. Search exact `normalized_headword`.
3. If no exact match exists, check exact `base_normalized_headword`.
4. Follow `file` and `anchor`.
5. Inspect the complete Markdown record.
6. Read `verification_status` and `boundary_confidence` before using the wording.
7. Attribute Hezareh only after inspecting `Source text`.

The index is navigation, not lexical evidence.

## Evidence rules

- `visually_checked`: supplied package marks the record visually checked. Preserve that status; do not imply a new check occurred.
- `raw_ocr`: OCR-derived. Verify against the original page when a consequential translation decision depends on exact wording.
- `hint_only`: page/navigation hint only. It must not be cited as Hezareh lexical evidence unless the source is checked and an entry is actually established.
- Duplicate normalized headwords are preserved, not collapsed.

## Reference-account format

When a usable record is found:

`Hezareh — <headword> — <record_id> — PDF p. <page> — <verification_status>/<boundary_confidence> — <file>#<anchor> — finding — effect`

When no safe entry is available:

`Hezareh — <headword> — exact entry unavailable / hint_only / lookup incomplete — verification needed`

## QC

- `qc/build-validation.json`
- `qc/verification-summary.json`
- `qc/hint-only-records.csv`
- `qc/low-confidence-records.csv`
- `qc/duplicate-normalized-headwords.csv`

No source wording is silently repaired in this layer.
