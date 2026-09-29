# Najafi retrieval layer

This directory is the Translation project's navigation and verified-entry layer for Abolhasan Najafi's *غلط ننویسیم*.

## Canonical source

`sources/Najafi — غلط ننویسیم.pdf`

The active canonical source is the clearer 480-page scan. The scanned page image is authoritative. The PDF has no usable Persian text layer, so extracted/OCR text must never be treated as Najafi's wording.

## Two navigation layers

### Visually verified body-heading layer

`index/headwords-master.csv` contains headings checked directly against dictionary-body pages.

Current manually verified coverage:
- PDF pages 13–30
- printed pages 1–18
- 57 verified heading rows

### Complete printed source-index layer

Najafi's own printed **فهرست راهنما** is present on PDF pages 449–478 (printed pages 437–466).

It is digitized for navigation as:
- `index/source-index-master.csv`
- `index/source-index-page-map.csv`

Current complete candidate coverage:
- 2727 source-index candidate rows
- all 30 printed source-index pages represented
- review/low-confidence rows are isolated in `qc/source-index-review-needed.csv`

Because the scan has no usable Persian text layer, OCR was used only as a last-resort way to digitize the printed source index. OCR here is navigation, never evidence.

## Evidence rule

**Navigation is not evidence.**

Before attributing any usage judgment to Najafi:
1. locate the candidate in the verified layer or complete source-index layer;
2. open the corresponding dictionary-body page in the canonical PDF;
3. visually verify the actual heading and entry;
4. only then report Najafi's finding;
5. if the entry becomes recurrently useful, add a faithful verified transcription under `entries/`.

Reference-account form:

`Najafi — «<headword>» — PDF p. <pdf_page> / printed p. <printed_page> — visually_checked — finding — effect on translation`

## Lookup

Use:
`tools/najafi_lookup.py <Persian query>`

Lookup order:
1. exact verified body-heading match;
2. exact source-index candidate;
3. fuzzy source-index candidates;
4. visual source-index/body inspection when machine navigation remains uncertain.

## Completion state

**Phase 1 navigation is complete.**

Full-entry transcription remains intentionally incremental by actual translation need. This avoids creating a large unverified OCR corpus while keeping the entire book navigable.
